import os
import json
from pathlib import Path
from cloudgpt_aoai import get_chat_completion
from alive_progress import alive_bar, config_handler
from tqdm import tqdm
import re

config_handler.set_global(length=40, spinner='fish', spinner_length=10, force_tty=True)

def collect_java_files(src_main_path):
    """collect all java files"""
    java_files = {}
    
    print(f"Scanning directory: {src_main_path}")
    # calculate total file number
    total_files = sum(1 for root, _, files in os.walk(src_main_path)
                     for file in files if file.endswith('.java'))
    print(f"Found {total_files} Java files")
    
    with alive_bar(total_files, title='Collecting Java files') as bar:
        for root, _, files in os.walk(src_main_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            relative_path = os.path.relpath(file_path, src_main_path)
                            java_files[relative_path] = f.read()
                            print(f"Read file: {relative_path}")
                    except Exception as e:
                        print(f"Error reading file {file_path}: {str(e)}")
                    bar()
    
    return java_files

def fix_json_escapes(json_str):
    """修复 JSON 中的非法转义字符"""
    return re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)

def translate_code(java_files):
    """use LLM to translate Java code into C#"""
    print(f"Starting translation for {len(java_files)} files")
    system_message = """You are a code translator. Please translate the provided Java code into C# code. 
    For any external dependencies or methods not defined in the repository:
    1. Use appropriate C# built-in alternatives
    2. Maintain the same functionality
    3. Follow C# naming conventions
    4. Return ONLY a valid JSON object where keys are file paths and values are translated C# code.
    5. DO NOT include any explanatory text before or after the JSON.
    
    Example response format:
    {
        "Example.cs": "namespace Example { ... }",
        "Another.cs": "namespace Another { ... }"
    }"""

    # construct complete Java code prompt
    files_content = ""
    print("Preparing files for translation...")
    for file_path, content in java_files.items():
        files_content += f"\nFile: {file_path}\n```java\n{content}\n```\n"
        print(f"Added file to translation batch: {file_path}")

    user_message = f"""Please translate these Java files to C#:
    {files_content}
    
    Return ONLY a valid JSON object where keys are file paths (change .java to .cs) and values are the translated C# code."""

    chat_message = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    print("Sending request to LLM...")
    response = get_chat_completion(
        engine="gpt-4o-mini-20240718",
        messages=chat_message,
    )

    print("Received response from LLM")
    response_text = response.choices[0].message.content.strip()
    
    # Clean up response text
    response_text = response_text.replace('```json', '').replace('```', '')
    
    # Try to find JSON content if there's additional text
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rstrip().rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx]
    except Exception as e:
        print(f"Error cleaning response text: {str(e)}")
    
    try:
        # 在解析 JSON 之前修复转义字符
        fixed_response = fix_json_escapes(response_text)
        translated = json.loads(fixed_response)
        
        print(f"Successfully parsed JSON response with {len(translated)} files")
        # Validate the structure
        if not isinstance(translated, dict):
            raise ValueError("Response is not a dictionary")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in translated.items()):
            raise ValueError("Invalid response structure")
        return translated
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {str(e)}")
        print("Invalid JSON content:", response_text)
        # 在出错时保存响应内容以便调试
        with open('failed_response.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise

def save_csharp_files(translated_code, output_path):
    """save translated C# codes"""
    print(f"Saving {len(translated_code)} C# files to {output_path}")
    file_count = 0
    
    for file_path, content in translated_code.items():
        # replace .java with .cs
        cs_file_path = file_path.replace('.java', '.cs')
        full_path = os.path.join(output_path, cs_file_path)
        
        # create corresponding path
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        try:
            # save file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            file_count += 1
            print(f"Saved file {file_count}: {full_path}")
        except Exception as e:
            print(f"Error saving file {full_path}: {str(e)}")

    print(f"Successfully saved {file_count} files")

def save_json_response(translated_code, output_path, repo_name):
    """save translation result as JSON"""
    json_file_path = os.path.join(output_path, f"{repo_name}_translation.json")
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(translated_code, f, indent=2, ensure_ascii=False)
        print(f"JSON response saved to: {json_file_path}")
    except Exception as e:
        print(f"Error saving JSON response: {str(e)}")

def process_repo(input_path, output_path):
    """process a single repo"""
    print(f"\nProcessing repository:")
    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    
    # make output dir
    try:
        os.makedirs(output_path, exist_ok=True)
        print(f"Created output directory: {output_path}")
    except Exception as e:
        print(f"Error creating output directory: {str(e)}")
        return
    
    repo_name = os.path.basename(input_path)
    
    # get src/main dir path
    src_main_path = os.path.join(input_path, 'src', 'main')
    if not os.path.exists(src_main_path):
        print(f"Warning: {src_main_path} does not exist")
        # Try finding any .java files in the input path
        java_files = []
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        if java_files:
            print(f"Found {len(java_files)} Java files in alternative locations")
            src_main_path = input_path
        else:
            return
    
    # collect Java files
    java_files = collect_java_files(src_main_path)
    if not java_files:
        print(f"Warning: No Java files found in {src_main_path}")
        return
    
    print(f"Collected {len(java_files)} Java files")
    
    # translation
    try:
        translated_code = translate_code(java_files)
        # save JSON response
        save_json_response(translated_code, output_path, repo_name)
        # save translated files
        save_csharp_files(translated_code, output_path)
        print(f"Successfully processed repo: {repo_name}")
    except Exception as e:
        print(f"Error processing repo {repo_name}: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def main(input_base_path=None, output_base_path=None):
    """process all repos under input base path"""
    input_base_path = input_base_path or os.environ.get('INPUT_PATH')
    output_base_path = output_base_path or os.environ.get('OUTPUT_PATH')
    
    if not input_base_path:
        input_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/java/repos")
    if not output_base_path:
        output_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output/java2csharp/repos")
    
    print(f"Starting processing with:")
    print(f"Input base path: {input_base_path}")
    print(f"Output base path: {output_base_path}")
    
    repos = [repo for repo in os.listdir(input_base_path) 
            if os.path.isdir(os.path.join(input_base_path, repo))]
    
    print(f"Found {len(repos)} repositories to process")
    
    for repo in tqdm(repos, desc='Processing repositories'):
        repo_path = os.path.join(input_base_path, repo)
        if os.path.isdir(repo_path):
            output_repo_path = os.path.join(output_base_path, repo)
            print(f"\nProcessing repo: {repo}")
            process_repo(repo_path, output_repo_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Translate Java repositories to C#')
    parser.add_argument('--input', help='Input directory containing Java repositories')
    parser.add_argument('--output', help='Output directory for translated C# code')
    args = parser.parse_args()
    
    print("Script started")
    
    input_path = args.input
    output_path = args.output
    
    # verify paths exist
    if input_path:
        print(f"Input path exists: {os.path.exists(input_path)}")
    if output_path:
        print(f"Output path exists: {os.path.exists(output_path)}")
    
    main(input_path, output_path)