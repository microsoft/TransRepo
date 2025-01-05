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
    return re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)

def collect_skeleton_files(skeleton_path, java_files):
    """collect corresponding skeleton files for java files"""
    skeleton_files = {}
    
    print(f"Collecting skeleton files from: {skeleton_path}")
    for java_path in java_files.keys():
        # Convert .java to .cs for skeleton path
        skeleton_file_path = skeleton_path + "/src/main/" + java_path.replace('.java', '.cs')
        print(f"[DEBUG]:skeleton file path is {skeleton_file_path}")
        if os.path.exists(skeleton_file_path):
            try:
                with open(skeleton_file_path, 'r', encoding='utf-8') as f:
                    skeleton_files[java_path] = f.read()
                    print(f"Found skeleton file for: {java_path}")
            except Exception as e:
                print(f"Error reading skeleton file {skeleton_file_path}: {str(e)}")
        else:
            print(f"Warning: No skeleton file found for {java_path}")
            skeleton_files[java_path] = None
    
    return skeleton_files

def fix_json_escapes(json_str):
    import re
    
    json_str = json_str.strip()
    
    lines = json_str.split('\n')
    fixed_lines = []
    in_string = False
    
    for line in lines:
        if in_string:
            line = line.replace('\\', '\\\\')
            line = line.replace('"', '\\"')
            fixed_lines.append(line)
            if line.rstrip().endswith('"'):
                in_string = False
        else:
            quote_count = line.count('"') - line.count('\\"')
            if quote_count % 2 == 1:
                in_string = True
            fixed_lines.append(line)
    
    json_str = '\n'.join(fixed_lines)
    
    json_str = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)
    
    json_str = json_str.rstrip()
    if not json_str.endswith('}'):
        json_str += '}'
    if not json_str.endswith('"}'):
        json_str = json_str.rstrip('"') + '"}'
    
    return json_str

def translate_code(java_files, skeleton_files):
    """use LLM to translate Java code into C# code with skeleton guidance"""
    print(f"Starting translation for {len(java_files)} files")
    system_message = """You are a code translator. Please translate the provided Java code into C# code.
    For each file, you will be provided with:
    1. The original Java code
    2. A C# skeleton file containing the correct interface, namespace, and class structure
    
    Your task is to:
    1. Fill in the implementation logic in the C# skeleton while maintaining the existing structure
    2. Keep all namespace, class, and interface declarations from the skeleton
    3. Ensure the implementation follows C# conventions and uses appropriate C# alternatives
    4. Return ONLY a valid JSON object where keys are file paths and values are the completed C# code
    5. DO NOT include any explanatory text before or after the JSON
    
    Example response format:
    {
        "Example.cs": "namespace Example { ... }",
        "Another.cs": "namespace Another { ... }"
    }"""

    # construct complete prompt with Java code and skeletons
    files_content = ""
    print("Preparing files for translation...")
    for file_path, java_content in java_files.items():
        skeleton_content = skeleton_files.get(file_path)
        files_content += f"\nFile: {file_path}\n"
        files_content += f"Original Java code:\n```java\n{java_content}\n```\n"
        if skeleton_content:
            files_content += f"C# Skeleton to fill in:\n```csharp\n{skeleton_content}\n```\n"
        else:
            files_content += "No skeleton file available for this path.\n"
        print(f"Added file to translation batch: {file_path}")

    user_message = f"""Please translate these Java files to C# by filling in the implementation logic in the provided skeletons:
    {files_content}
    
    Important:
    1. Maintain the exact namespace, class, and interface structure from the skeleton files
    2. Only fill in the implementation logic
    3. Keep all existing using statements and class/interface declarations
    4. Return ONLY a valid JSON object where keys are file paths (with .cs extension) and values are the completed C# code."""

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
        engine="gpt-4o-20240513",
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
        # Fix JSON escapes before parsing
        fixed_response = fix_json_escapes(response_text)
        
        try:
            translated = json.loads(fixed_response)
        except json.JSONDecodeError as e:
            print(f"First attempt to parse JSON failed: {str(e)}")
            fixed_response = re.sub(r'([^\\])"([^"]*$)', r'\1"\2"', fixed_response)
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
        with open('failed_response.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)
        try:
            pattern = r'\{[^{}]*\}'
            matches = re.finditer(pattern, response_text)
            partial_responses = {}
            for match in matches:
                try:
                    obj = json.loads(match.group())
                    if isinstance(obj, dict):
                        partial_responses.update(obj)
                except:
                    continue
            if partial_responses:
                print(f"Retrieved {len(partial_responses)} partial translations")
                return partial_responses
        except:
            pass
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


def save_csharp_files(translated_code, output_path: Path, src_main_path: Path):
    """save translated C# codes, maintaining the same directory structure as Java files"""
    output_path = Path(output_path)
    src_main_path = Path(src_main_path)
    print(f"Saving {len(translated_code)} C# files to {output_path}")
    file_count = 0
    
    for java_path, content in translated_code.items():
        java_file_path = java_path.replace('.cs', '.java')
        
        full_java_path = None
        for root, _, files in os.walk(src_main_path):
            current_path = Path(root) / java_file_path
            if current_path.exists():
                full_java_path = current_path
                break
        
        if full_java_path:
            rel_path = full_java_path.relative_to(src_main_path)
            
            output_file_path = output_path / 'src' / 'main' / rel_path.parent / f"{rel_path.stem}.cs"
        else:
            java_rel_path = Path(java_file_path)
            output_file_path = output_path / 'src' / 'main' / java_rel_path.parent / f"{java_rel_path.stem}.cs"
        
        print(f"[DEBUG]: Original path: {java_path}")
        print(f"[DEBUG]: Output path: {output_file_path}")
        
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            output_file_path.write_text(content, encoding='utf-8')
            file_count += 1
            print(f"Saved file {file_count}: {output_file_path}")
        except Exception as e:
            print(f"Error saving file {output_file_path}: {str(e)}")

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

def batch_process_files(java_files, skeleton_files, batch_size=5):
    all_results = {}
    file_items = list(java_files.items())
    
    for i in range(0, len(file_items), batch_size):
        batch_files = dict(file_items[i:i+batch_size])
        batch_skeletons = {k: skeleton_files[k] for k in batch_files.keys() if k in skeleton_files}
        
        try:
            batch_results = translate_code(batch_files, batch_skeletons)
            all_results.update(batch_results)
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
            for file_path, content in batch_files.items():
                try:
                    single_result = translate_code({file_path: content}, 
                                                {file_path: skeleton_files.get(file_path)})
                    all_results.update(single_result)
                except Exception as e2:
                    print(f"Failed to process file {file_path}: {str(e2)}")
                    
    return all_results

def process_repo(input_path, output_path, skeleton_base_path):
    """process a single repo"""
    print(f"\nProcessing repository:")
    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    print(f"Skeleton path: {skeleton_base_path}")
    input_path = Path(input_path)
    output_path = Path(output_path)
    skeleton_base_path = Path(skeleton_base_path)
    
    # make output dir
    try:
        os.makedirs(output_path, exist_ok=True)
        print(f"Created output directory: {output_path}")
    except Exception as e:
        print(f"Error creating output directory: {str(e)}")
        return
    
    repo_name = os.path.basename(input_path)
    skeleton_path = os.path.join(skeleton_base_path, repo_name)
    
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
    
    # collect corresponding skeleton files
    skeleton_files = collect_skeleton_files(skeleton_path, java_files)
    print(f"Collected {len(java_files)} Java files and {len(skeleton_files)} skeleton files")
    
    try:
        translated_code = batch_process_files(java_files, skeleton_files)
        save_json_response(translated_code, output_path, repo_name)
        save_csharp_files(translated_code, output_path, Path(src_main_path))
        print(f"Successfully processed repo: {repo_name}")
    except Exception as e:
        print(f"Error processing repo {repo_name}: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def main(input_base_path, output_base_path, skeleton_base_path):
    """process all repos under input base path"""
    print(f"Starting processing with:")
    print(f"Input base path: {input_base_path}")
    print(f"Output base path: {output_base_path}")
    print(f"Skeleton base path: {skeleton_base_path}")
    
    repos = [repo for repo in os.listdir(input_base_path) 
            if os.path.isdir(os.path.join(input_base_path, repo))]
    
    print(f"Found {len(repos)} repositories to process")
    
    for repo in tqdm(repos, desc='Processing repositories'):
        repo_path = os.path.join(input_base_path, repo)
        if os.path.isdir(repo_path):
            output_repo_path = os.path.join(output_base_path, repo)
            print(f"\nProcessing repo: {repo}")
            process_repo(repo_path, output_repo_path, skeleton_base_path)

if __name__ == "__main__":
    INPUT_PATH = ""
    OUTPUT_PATH = ""
    SKELETON_PATH = ""  # Add your skeleton path here
    
    print("Script started")
    print(f"Input path exists: {os.path.exists(INPUT_PATH)}")
    print(f"Output path exists: {os.path.exists(OUTPUT_PATH)}")
    print(f"Skeleton path exists: {os.path.exists(SKELETON_PATH)}")
    
    main(INPUT_PATH, OUTPUT_PATH, SKELETON_PATH)