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

from baseline.initial_translate import process_project
from baseline.java2csharp import translate_code, get_chat_completion, collect_java_files, save_csharp_files
from verify.translated_code_validator import copy_skeleton_and_run_test

"""
Usage:
This script optimizes Java to C# code translation using test feedback.

Key features:
1. Performs initial Java to C# translation
2. Runs tests on translated code
3. Iteratively improves translation based on test results
4. Handles JSON response parsing and error recovery
5. Maintains optimization history

Example command:
python3 optimize_translation.py \
--input-path "/path/to/java/source" \
--skeleton-path "/path/to/csharp/skeleton" \
--output-path "/path/to/output" \
--test-config "/path/to/test/config.json"

Required arguments:
--input-path: Path to Java source directory
--output-path: Path for C# output
--skeleton-path: Path to C# project skeleton  
--test-config: Path to test configuration JSON
--max-iterations: Maximum optimization iterations (default=3)
"""

def fix_json_escapes(json_str):
    """Fix invalid escape sequences in JSON string"""
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
    """Create prompt for optimization iteration using failed test info"""
    system_message = """You are a C# code specialist. You are debugging a C# repo which has compiling/functional errors.
    Please fix the C# codes based on the provided build/test errors.
    
    CRITICAL: Return ONLY a valid JSON object where keys are file paths and values are translated C# code. WITHOUT any markdown formatting or code blocks.
    The response should be a plain JSON object that can be directly parsed.

    Example response format (without code blocks or other formatting):
    {
    "File1.cs": "namespace Example { ... }",
    "File2.cs": "namespace Another { ... }"
    }"""
    
    # Read all .cs files under src/main in current iteration folder
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

def extract_json_content(text: str) -> str:
    """Extract JSON content using regex pattern matching"""
    # Match outermost curly braces and content
    json_pattern = r'\{(?:[^{}]|(?R))*\}'
    matches = re.finditer(json_pattern, text, re.DOTALL)
    
    # Get longest match
    longest_match = ''
    for match in matches:
        if len(match.group()) > len(longest_match):
            longest_match = match.group()
    
    return longest_match if longest_match else text

def clean_json_string(text: str) -> str:
    """Clean and normalize JSON string"""
    # Remove common interfering characters
    text = re.sub(r'```\w*\n?', '', text)  # Remove code block markers
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove extra blank lines
    text = text.strip()
    
    # Fix common JSON format issues
    text = text.replace('\\"', '"')  # Fix escaped quotes
    text = text.replace('\\n', '\n')  # Fix newlines 
    text = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', text)  # Fix invalid escape chars
    
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
        # Get LLM response
        response = get_chat_completion(
            engine="gpt-4o-mini-20240718",
            messages=messages,
        )
        print("Received response from LLM")
        
        if not response or not hasattr(response, 'choices') or not response.choices:
            raise ValueError("Invalid response format from LLM")
            
        # Extract and clean response text
        response_text = response.choices[0].message.content.strip()
        response_text = response_text.replace('```json', '').replace('```', '')

        # Extract JSON content
        start_idx = response_text.find('{')
        end_idx = response_text.rstrip().rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx]
        
        # Try parsing JSON
        try:
            translated = json.loads(response_text)
        except json.JSONDecodeError:
            # Try fixing JSON and parse again
            fixed_response = fix_json_escapes(response_text)
            translated = json.loads(fixed_response)
        
        # Validate response structure
        if not isinstance(translated, dict):
            raise ValueError("Response is not a dictionary")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in translated.items()):
            raise ValueError("Invalid response structure")
            
        print(f"Successfully parsed JSON response with {len(translated)} files")
        return translated
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        # Save failed response
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
            # Delete all files in iteration_1 directory if exists
            if os.path.exists(iteration_path):
                shutil.rmtree(iteration_path)
            # Copy initial_translation directory to iteration_1
            shutil.copytree(initial_translation_path, iteration_path)
        else:
            # Save current translation for other iterations
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
    """Main function to run translation optimization process"""
    parser = argparse.ArgumentParser(description='Optimize Java to C# translation using test feedback')
    parser.add_argument('--input-path', required=True, help='Path to Java source directory')
    parser.add_argument('--output-path', required=True, help='Path for C# output')
    parser.add_argument('--skeleton-path', required=True, help='Path to C# project skeleton')
    parser.add_argument('--test-config', required=True, help='Path to test configuration JSON')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum optimization iterations')
    
    args = parser.parse_args()
    
    print("\n=== Starting Translation Optimization Process ===")
    
    # Create initial translation directory
    initial_translation_path = Path(args.output_path) / "initial_translation"
    initial_translation_path.mkdir(parents=True, exist_ok=True)
    
    # Create dependency analysis directory
    dependency_path = Path(args.output_path) / "dependencies"
    dependency_path.mkdir(parents=True, exist_ok=True)
    
    # Perform initial translation
    print("\nPerforming initial translation...")
    java_root = Path(args.input_path)
    cs_root = Path(args.skeleton_path)
    
    # Get project name (assume last part of input path is project name)
    project_name = java_root.name
    
    # Use process_project for initial translation
    # process_project(
    #     java_root=java_root,
    #     cs_root=cs_root,
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
    
    # Create output directory
    os.makedirs(args.output_path, exist_ok=True)
    
    # Optimize translation
    final_translation, optimization_history = optimize_translation(
        initial_translation=initial_translation,
        skeleton_path=args.skeleton_path,
        json_path=args.test_config,
        output_base_path=args.output_path,
        max_iterations=args.max_iterations
    )
    
    # Save optimization history
    history_path = os.path.join(args.output_path, 'optimization_history.json')
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(optimization_history, f, indent=2)
    
    print(f"\n✓ Optimization complete. Results saved to: {args.output_path}")
    print(f"✓ Optimization history saved to: {history_path}")

if __name__ == "__main__":
    main()

# Example command:
# python3 optimize_translation.py \
# --input-path "/home/v-jiahengwen/RepoTranslationAgent/data/java/hutool-test/hutool-script" \
# --skeleton-path "/home/v-jiahengwen/RepoTranslationAgent/output/skeleton/c_sharp/hutool-test/hutool-script" \
# --output-path "/home/v-jiahengwen/RepoTranslationAgent/output/java2csharp/validation/test-script" \
# --test-config "/home/v-jiahengwen/RepoTranslationAgent/output/dependency/hutool-script/test_dependency.json"

# File path examples:
# /home/v-jiahengwen/RepoTranslationAgent/output/java2csharp/validation/test-script/iteration_2/src/main/java/cn/hutool/script/Hutool.Script/ScriptUtil.cs
# /home/v-jiahengwen/RepoTranslationAgent/output/java2csharp/validation/test-script/iteration_2/java/cn/hutool/script/Hutool.Script/ScriptUtil.cs