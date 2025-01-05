import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from tqdm import tqdm
import argparse
import shutil
from dependency_analyzer import DependencyAnalyzer
from openai import OpenAI

sys.path.append(str(Path(__file__).parent.parent))

from baseline.baseline_translate import process_project
from baseline.java2csharp import translate_code, get_chat_completion, collect_java_files, save_csharp_files
from verify.translated_code_validator import copy_skeleton_and_run_test

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
    json_pattern = r'\{(?:[^{}]|(?R))*\}'
    matches = re.finditer(json_pattern, text, re.DOTALL)
    
    longest_match = ''
    for match in matches:
        if len(match.group()) > len(longest_match):
            longest_match = match.group()
    
    return longest_match if longest_match else text

def clean_json_string(text: str) -> str:
    """Clean and normalize JSON string"""
    text = re.sub(r'```\w*\n?', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()
    
    text = text.replace('\\"', '"')
    text = text.replace('\\n', '\n')
    text = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', text)
    
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
        response = get_chat_completion(
        engine="gpt-4o-mini-20240718",
        messages=messages,
        )
        print("Received response from LLM")
        if not response or not hasattr(response, 'choices') or not response.choices:
            raise ValueError("Invalid response format from LLM")
            
        response_text = response.choices[0].message.content.strip()
        response_text = response_text.replace('```json', '').replace('```', '')

        start_idx = response_text.find('{')
        end_idx = response_text.rstrip().rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx]
        
        try:
            translated = json.loads(response_text)
        except json.JSONDecodeError:
            fixed_response = fix_json_escapes(response_text)
            translated = json.loads(fixed_response)
        
        if not isinstance(translated, dict):
            raise ValueError("Response is not a dictionary")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in translated.items()):
            raise ValueError("Invalid response structure")
            
        print(f"Successfully parsed JSON response with {len(translated)} files")
        return translated
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        try:
            with open('failed_response.txt', 'w', encoding='utf-8') as f:
                f.write(response_text)
        except Exception as write_error:
            print(f"Failed to save error response: {str(write_error)}")
        raise

# def translate_code_with_feedback(messages: List[Dict[str, str]]) -> Dict[str, str]:
#     """Use optimized prompt to fix the code with improved error handling"""
#     response_text = ""
#     try:
#         client = OpenAI(
#             api_key="sk-DyNFnsXcgwk2UvvD1162F5D88a5a4b79Ba38Af92499e4e42",
#             base_url="https://api.ai-gaochao.cn/v1"
#         )
        
#         # get LLM response
#         response = client.chat.completions.create(
#             model="claude-3-5-sonnet-20240620",
#             temperature=0,
#             messages=messages
#         )
#         print("Received response from LLM")
        
#         if not response or not hasattr(response, 'choices') or not response.choices:
#             raise ValueError("Invalid response format from LLM")
            
#         response_text = response.choices[0].message.content.strip()
#         response_text = response_text.replace('```json', '').replace('```', '')

#         start_idx = response_text.find('{')
#         end_idx = response_text.rstrip().rfind('}') + 1
        
#         if start_idx != -1 and end_idx != -1:
#             response_text = response_text[start_idx:end_idx]
        
#         try:
#             translated = json.loads(response_text)
#         except json.JSONDecodeError:
#             fixed_response = fix_json_escapes(response_text)
#             translated = json.loads(fixed_response)
        
#         if not isinstance(translated, dict):
#             raise ValueError("Response is not a dictionary")
#         if not all(isinstance(k, str) and isinstance(v, str) for k, v in translated.items()):
#             raise ValueError("Invalid response structure")
            
#         print(f"Successfully parsed JSON response with {len(translated)} files")
#         return translated
        
#     except Exception as e:
#         print(f"Error processing response: {str(e)}")
#         try:
#             with open('failed_response.txt', 'w', encoding='utf-8') as f:
#                 f.write(response_text)
#         except Exception as write_error:
#             print(f"Failed to save error response: {str(write_error)}")
#         raise

def find_related_errors(file_path: str, failed_tests: Dict[str, str]) -> List[str]:
    """Find errors related to a specific file from test outputs"""
    related_errors = []
    file_name = os.path.basename(file_path)
    
    for test_name, error_content in failed_tests.items():
        error_blocks = error_content.split('\n\n')
        
        for block in error_blocks:
            lines = block.strip().split('\n')
            is_related = False
            
            if lines and (file_path in lines[0] or file_name in lines[0]):
                is_related = True
            else:
                for line in lines:
                    if file_path in line or file_name in line:
                        is_related = True
                        break
            
            if is_related:
                related_errors.append(f"{test_name}:\n{block}")
    print(f"[RELATED ERROR DUBUGING]: The related error of {file_name} is {related_errors}")
    return related_errors

def extract_code_identifiers(file_content: str) -> Set[str]:
    identifiers = set()
    
    class_pattern = r'class\s+(\w+)'
    identifiers.update(re.findall(class_pattern, file_content))
    
    method_pattern = r'(?:public|private|protected|internal|\s)\s+\w+\s+(\w+)\s*\('
    identifiers.update(re.findall(method_pattern, file_content))
    
    property_pattern = r'(?:public|private|protected|internal|\s)\s+\w+\s+(\w+)\s*{\s*get'
    identifiers.update(re.findall(property_pattern, file_content))
    
    return identifiers

def find_related_errors_improved(file_path: str, file_content: str, failed_tests: Dict[str, str]) -> List[str]:
    related_errors = []
    file_name = os.path.basename(file_path)
    identifiers = extract_code_identifiers(file_content)
    
    for test_name, error_content in failed_tests.items():
        error_blocks = error_content.split('\n\n')
        
        for block in error_blocks:
            lines = block.strip().split('\n')
            is_related = False
            
            for line in lines:
                if file_path in line or file_name in line:
                    is_related = True
                    break
                    
                for identifier in identifiers:
                    if identifier in line:
                        is_related = True
                        break
                
                if check_error_lib_not_found(line) or \
                   check_error_class_not_found(line) or \
                   check_error_no_definition(line):
                    for identifier in identifiers:
                        if identifier in line:
                            is_related = True
                            break
            
            if is_related:
                related_errors.append(f"{test_name}:\n{block}")
    
    return related_errors

def create_single_file_prompt(file_path: str, file_content: str, related_errors: List[str]) -> List[Dict[str, str]]:
    """Create a prompt for optimizing a single file"""
    system_message = """You are a C# code specialist. You are debugging a C# repo which has compiling/functional errors.
    Please fix the specific C# file based on the provided build/test errors.
    
    CRITICAL: Return ONLY the corrected C# code, without any markdown formatting, explanations, or introductory text.
    Do not use code blocks or any other formatting - just return the raw C# code."""
    
    user_message = f"""Fix the following C# file based on the related errors:

    File: {file_path}
    Current code:
    {file_content}

    Related Errors:
    {chr(10).join(related_errors)}"""

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

def optimize_file(file_path: str, 
                 file_content: str, 
                 related_errors: List[str]) -> Optional[str]:
    """Optimize a single file using LLM"""
    try:
        prompt = create_single_file_prompt(file_path, file_content, related_errors)
        response = get_chat_completion(
            engine="gpt-4-visual-preview",
            messages=prompt,
        )
        
        if not response or not hasattr(response, 'choices') or not response.choices:
            return None
            
        return response.choices[0].message.content.strip()
            
    except Exception as e:
        print(f"Error optimizing file {file_path}: {str(e)}")
        return None

def optimize_translation(initial_translation: Dict[str, str],
                        skeleton_path: str,
                        json_path: str,
                        output_base_path: str,
                        max_iterations: int = 3) -> Tuple[Dict[str, str], List[Dict]]:
    """Iteratively optimize the code translation file by file"""
    current_translation = initial_translation
    iteration = 0
    optimization_history = []
    
    save_json_response(initial_translation, output_base_path, 'translation_initial.json')
    
    while iteration < max_iterations:
        print(f"\n=== Starting optimization iteration {iteration + 1}/{max_iterations} ===")
        
        iteration_path = os.path.join(output_base_path, f"iteration_{iteration + 1}")
        os.makedirs(iteration_path, exist_ok=True)
        
        if iteration == 0:
            initial_translation_path = os.path.join(output_base_path, "initial_translation")
            if os.path.exists(iteration_path):
                shutil.rmtree(iteration_path)
            shutil.copytree(initial_translation_path, iteration_path)
        else:
            save_csharp_files(current_translation, iteration_path)

        test_results = copy_skeleton_and_run_test(
            skeleton_path=skeleton_path,
            translated_path=iteration_path,
            json_path=json_path,
            output_base_path=os.path.join(output_base_path, f"test_iteration_{iteration + 1}")
        )  
        
        iteration_record = {
            'iteration': iteration + 1,
            'test_results': test_results
        }
        optimization_history.append(iteration_record)
        
        failed_tests = analyze_test_results(test_results)
        save_error_info(failed_tests, output_base_path, iteration + 1)
        
        if not failed_tests:
            print("\n✓ All tests passed!")
            save_json_response(current_translation, output_base_path, 'translation_final.json')
            return current_translation, optimization_history
            
        print(f"\n✗ Found {len(failed_tests)} failed tests. Attempting to fix file by file...")
        
        # New optimization logic - process each file individually
        new_translation = {}
        for file_path, content in current_translation.items():
            related_errors = find_related_errors(file_path, failed_tests)
            
            if related_errors:
                print(f"\nOptimizing {file_path} with {len(related_errors)} related errors")
                optimized_content = optimize_file(file_path, content, related_errors)
                if optimized_content:
                    new_translation[file_path] = optimized_content
                else:
                    new_translation[file_path] = content  # Keep original if optimization fails
            else:
                new_translation[file_path] = content  # Keep files without errors unchanged
        
        current_translation = new_translation
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
        
        # # Use process_project for initial translation
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