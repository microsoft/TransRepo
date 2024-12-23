import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm
import argparse
import shutil
from dependency_analyzer import DependencyAnalyzer

sys.path.append(str(Path(__file__).parent.parent))

from baseline.baseline_translate import process_project
from baseline.java2csharp import translate_code, get_chat_completion, collect_java_files, save_csharp_files
from verify.translated_code_validator import copy_skeleton_and_run_test

class APIStats:
    def __init__(self):
        self.call_count = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
    
    def update_stats(self, response):
        self.call_count += 1
        # 假设response对象包含token统计信息
        if hasattr(response, 'usage'):
            self.total_prompt_tokens += response.usage.prompt_tokens
            self.total_completion_tokens += response.usage.completion_tokens
            # 可以根据不同模型设置不同的价格
            prompt_cost = (response.usage.prompt_tokens / 1000) * 0.03  # GPT-4定价
            completion_cost = (response.usage.completion_tokens / 1000) * 0.06
            self.total_cost += prompt_cost + completion_cost
    
    def print_stats(self):
        print(f"Total API calls: {self.call_count}")
        print(f"Total prompt tokens: {self.total_prompt_tokens}")
        print(f"Total completion tokens: {self.total_completion_tokens}")
        print(f"Total cost: ${self.total_cost:.4f}")

api_stats = APIStats()

def fix_json_escapes(json_str):
    return re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)

def save_json_response(translation: Dict[str, str], output_path: str, filename: str = 'translation_result.json'):
    """Save translation results to JSON file"""
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    result = {
        "translations": translation
    }
    
    json_path = os.path.join(output_path, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

def save_error_info(failed_tests: Dict[str, str], output_path: str, iteration: int):
    """Save error information for each iteration"""
    error_path = os.path.join(output_path, f'errors_iteration_{iteration}.txt')
    with open(error_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Errors from iteration {iteration} ===\n\n")
        for test_name, error in failed_tests.items():
            f.write(f"Test: {test_name}\n")
            f.write("Error:\n")
            f.write(f"{error}\n")
            f.write("-" * 80 + "\n\n")

def create_optimization_prompt(iteration_path: str, failed_tests: Dict[str, str]) -> List[Dict[str, str]]:
    system_message = """You are a C# code specialist. You are debugging a C# repo which has compiling/functional errors.
    Please fix the C# codes based on the provided build/test errors.
    
    CRITICAL: Return ONLY a valid JSON object where keys are file paths and values are translated C# code. WITHOUT any markdown formatting or code blocks.
    The response should be a plain JSON object that can be directly parsed.

    Example response format (without code blocks or other formatting):
    {
    "File1.cs": "namespace Example { ... }",
    "File2.cs": "namespace Another { ... }"
    }"""
    
    # 读取当前iteration文件夹中src/main下的所有.cs文件
    files_content = ""
    current_files = {}
    src_main_path = os.path.join(iteration_path, "src", "main")
    
    for root, _, files in os.walk(src_main_path):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                relative_path = os.path.join("src", "main", os.path.relpath(file_path, src_main_path))
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    current_files[relative_path] = content
                    files_content += f"\nFile: {relative_path}\n```csharp\n{content}\n```\n"
                    print(f"Added file to translation batch: {relative_path}")

    error_content = "\nBuild/Test Errors:\n"
    for test_name, errors in failed_tests.items():
        error_content += f"\nTest: {test_name}\n{errors}\n"

    user_message = f"""Fix the C# translations based on the test errors.

    {files_content}
    {error_content}

    Example:
    {{
    "FileA.cs": "namespace Example {{ ... }}",
    "FileB.cs": "namespace Another {{ ... }}"
    }}"""

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

def analyze_test_results(results: Dict) -> Dict[str, str]:
    """Extract error messages from test results"""
    failed_tests = {}
    
    for test_name, result in results.items():
        if 'error' in result:
            failed_tests[test_name] = result['error']
        elif result['build'] == 'failed':
            failed_tests[test_name] = result['build_error']
        elif result.get('test') == 'failed':
            failed_tests[test_name] = result['test_output']
    
    return failed_tests

from json.decoder import JSONDecodeError

def extract_json_content(text: str) -> str:
    """Extract JSON content using regex pattern matching"""
    # 匹配最外层的花括号及其内容
    json_pattern = r'\{(?:[^{}]|(?R))*\}'
    matches = re.finditer(json_pattern, text, re.DOTALL)
    
    # 获取最长的匹配结果
    longest_match = ''
    for match in matches:
        if len(match.group()) > len(longest_match):
            longest_match = match.group()
    
    return longest_match if longest_match else text

def clean_json_string(text: str) -> str:
    """Clean and normalize JSON string"""
    # 移除常见的干扰字符
    text = re.sub(r'```\w*\n?', '', text)  # 移除代码块标记
    text = re.sub(r'\n\s*\n', '\n', text)  # 移除多余空行
    text = text.strip()
    
    # 修正常见的JSON格式问题
    text = text.replace('\\"', '"')  # 修正转义引号
    text = text.replace('\\n', '\n')  # 修正换行符
    text = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', text)  # 修正无效的转义字符
    
    return text

def validate_json_structure(data: Dict[str, str]) -> bool:
    """Validate JSON structure meets requirements"""
    if not isinstance(data, dict):
        raise ValueError("Response must be a dictionary")
    
    for key, value in data.items():
        if not isinstance(key, str):
            raise ValueError(f"Invalid key type: {type(key)}, must be string")
        if not isinstance(value, str):
            raise ValueError(f"Invalid value type for key '{key}': {type(value)}, must be string")
    
    return True

def translate_code_with_feedback(messages: List[Dict[str, str]]) -> Dict[str, str]:
    """Use optimized prompt to fix the code with improved error handling"""
    try:
        # 获取LLM响应
        response = get_chat_completion(
            engine="gpt-4o-mini-20240718",
            messages=messages,
        )
        api_stats.update_stats(response)
        print("Received response from LLM")
        
        if not response or not hasattr(response, 'choices') or not response.choices:
            raise ValueError("Invalid response format from LLM")
            
        # 提取并清理响应文本
        response_text = response.choices[0].message.content.strip()
        response_text = response_text.replace('```json', '').replace('```', '')

        # 提取JSON内容
        start_idx = response_text.find('{')
        end_idx = response_text.rstrip().rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx]
        
        # 尝试解析JSON
        try:
            translated = json.loads(response_text)
        except json.JSONDecodeError:
            # 尝试修复JSON并重新解析
            fixed_response = fix_json_escapes(response_text)
            translated = json.loads(fixed_response)
        
        # 验证响应结构
        if not isinstance(translated, dict):
            raise ValueError("Response is not a dictionary")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in translated.items()):
            raise ValueError("Invalid response structure")
            
        print(f"Successfully parsed JSON response with {len(translated)} files")
        return translated
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        # 保存失败的响应
        try:
            with open('failed_response.txt', 'w', encoding='utf-8') as f:
                f.write(response_text)
        except Exception as write_error:
            print(f"Failed to save error response: {str(write_error)}")
        raise


def optimize_translation(initial_translation: Dict[str, str],
                        skeleton_path: str,
                        json_path: str,
                        output_base_path: str,
                        max_iterations: int = 3) -> Tuple[Dict[str, str], List[Dict]]:
    """Iteratively optimize the code translation"""
    current_translation = initial_translation
    iteration = 0
    optimization_history = []
    
    # Save initial translation
    save_json_response(initial_translation, output_base_path, 'translation_initial.json')
    
    while iteration < max_iterations:
        print(f"\n=== Starting optimization iteration {iteration + 1}/{max_iterations} ===")
        
        # Create iteration directory
        iteration_path = os.path.join(output_base_path, f"iteration_{iteration + 1}")
        os.makedirs(iteration_path, exist_ok=True)
        
        if iteration == 0:
            initial_translation_path = os.path.join(output_base_path, "initial_translation")
            print(f"The path to initial translation files is {initial_translation_path}")
            print(f"The path to iteration is {iteration_path}")
            # 删除iteration_1目录中的所有文件（如果存在）
            if os.path.exists(iteration_path):
                shutil.rmtree(iteration_path)
            # 复制initial_translation目录到iteration_1
            shutil.copytree(initial_translation_path, iteration_path)
        else:
            # 其他迭代正常保存当前翻译
            save_csharp_files(current_translation, iteration_path)

        # Run tests
        test_results = copy_skeleton_and_run_test(
            skeleton_path=skeleton_path,
            translated_path=iteration_path,
            json_path=json_path,
            output_base_path=os.path.join(output_base_path, f"test_iteration_{iteration + 1}")
        )  
        
        # Record iteration results
        iteration_record = {
            'iteration': iteration + 1,
            'test_results': test_results
        }
        optimization_history.append(iteration_record)
        
        # Analyze test results
        failed_tests = analyze_test_results(test_results)
        
        # Save error information
        save_error_info(failed_tests, output_base_path, iteration + 1)
        
        if not failed_tests:
            print("\n✓ All tests passed!")
            save_json_response(current_translation, output_base_path, 'translation_final.json')
            return current_translation, optimization_history
            
        print(f"\n✗ Found {len(failed_tests)} failed tests. Attempting to fix...")
        
        try:
            # Create optimization prompt with current iteration path
            optimization_prompt = create_optimization_prompt(
                iteration_path=iteration_path,
                failed_tests=failed_tests
            )
            
            # Attempt re-translation
            current_translation = translate_code_with_feedback(optimization_prompt)
            
            iteration_record['optimization_performed'] = True
            
        except Exception as e:
            print(f"\n❌ Error during optimization: {str(e)}")
            iteration_record['error'] = str(e)
            break
            
        iteration += 1
    
    print("\n⚠ Reached maximum iterations or encountered error")
    save_json_response(current_translation, output_base_path, 'translation_final.json')
    return current_translation, optimization_history

def main():
    parser = argparse.ArgumentParser(description='Optimize Java to C# translation using test feedback')
    parser.add_argument('--input-path', required=True, help='Path to Java source directory containing multiple projects')
    parser.add_argument('--output-path', required=True, help='Base path for C# output')
    parser.add_argument('--skeleton-path', required=True, help='Base path to C# project skeletons')
    parser.add_argument('--test-config', required=True, help='Path to test configuration JSON directory')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum optimization iterations')
    
    args = parser.parse_args()
    
    # Get all project folders under input directory
    java_base_path = Path(args.input_path)
    projects = [d.name for d in java_base_path.iterdir() if d.is_dir()]
    
    print(f"\n=== Found {len(projects)} projects to process: {', '.join(projects)} ===")
    
    # Process each project
    for project_name in projects:
        print(f"\n=== Processing project: {project_name} ===")
        
        # Construct project-related paths
        java_project_path = java_base_path / project_name
        skeleton_project_path = Path(args.skeleton_path) / project_name
        output_project_path = Path(args.output_path) / project_name
        test_config_file = Path(args.test_config) / f"{project_name}.json"
        
        # Verify that required paths and files exist
        if not all([java_project_path.exists(), skeleton_project_path.exists(), test_config_file.exists()]):
            print(f"Skipping {project_name}: Missing required paths or config file")
            continue
        
        # Create project output directory structure
        initial_translation_path = output_project_path / "initial_translation"
        dependency_path = output_project_path / "dependencies"
        initial_translation_path.mkdir(parents=True, exist_ok=True)
        dependency_path.mkdir(parents=True, exist_ok=True)
        
        # Perform initial translation
        print(f"\nPerforming initial translation for {project_name}...")
        
        # Use process_project for initial translation
        # process_project(
        #     java_root=java_project_path,
        #     cs_root=skeleton_project_path,
        #     output_root=initial_translation_path,
        #     dependency_root=dependency_path,
        #     project_name=project_name
        # )
        
        # Collect translated files
        initial_translation = {}
        for cs_file in initial_translation_path.rglob('*.cs'):
            relative_path = cs_file.relative_to(initial_translation_path)
            with open(cs_file, 'r', encoding='utf-8') as f:
                initial_translation[str(relative_path)] = f.read()
        
        print(f"\nInitial translation completed with {len(initial_translation)} files")
        
        # Create project output directory
        output_project_path.mkdir(parents=True, exist_ok=True)
        
        # Optimize translation
        final_translation, optimization_history = optimize_translation(
            initial_translation=initial_translation,
            skeleton_path=str(skeleton_project_path),
            json_path=str(test_config_file),
            output_base_path=str(output_project_path),
            max_iterations=args.max_iterations
        )
        
        # Save optimization history
        history_path = output_project_path / 'optimization_history.json'
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(optimization_history, f, indent=2)
        
        print(f"\n✓ Optimization complete for {project_name}. Results saved to: {output_project_path}")
        print(f"✓ Optimization history saved to: {history_path}")
        api_stats.print_stats()

if __name__ == "__main__":
    main()

# python3 optimize_translation.py \
# --input-path "/home/v-jiahengwen/RepoTranslationAgent/fixed_data/java_origin" \
# --skeleton-path "/home/v-jiahengwen/RepoTranslationAgent/fixed_data/c_sharp_skeleton" \
# --output-path "/home/v-jiahengwen/RepoTranslationAgent/fixed_data/validation" \
# --test-config "/home/v-jiahengwen/RepoTranslationAgent/fixed_data/test_dependency"


# /home/v-jiahengwen/RepoTranslationAgent/output/java2csharp/validation/test-script/iteration_2/src/main/java/cn/hutool/script/Hutool.Script/ScriptUtil.cs
# /home/v-jiahengwen/RepoTranslationAgent/output/java2csharp/validation/test-script/iteration_2/java/cn/hutool/script/Hutool.Script/ScriptUtil.cs