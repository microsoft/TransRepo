import os
import shutil
import argparse
import logging
from pathlib import Path
from typing import Dict, List
from cloudgpt_aoai import get_chat_completion

from dependency_analyzer import DependencyAnalyzer

def get_file_dependencies(dependency_file: Path, project_name: str, file_name: str) -> List[str]:
    """get dependency information for specific file"""
    if not dependency_file.exists():
        return []
        
    project_dep_file = dependency_file / f"{project_name}_dependency_analysis.txt"
    if not project_dep_file.exists():
        return []
    
    deps = []
    current_file = None
    
    with open(project_dep_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("File: "):
                current_file = line.replace("File: ", "")
            elif current_file == file_name and line.startswith("Calls: "):
                deps.append(line.replace("Calls: ", ""))
    
    return deps

def _parse_dependency_file(dep_file: Path) -> Dict[str, List[str]]:
    """return all dependency information for current file"""
    if not dep_file.exists():
        logging.warning(f"Dependency file not found: {dep_file}")
        return {}
        
    deps = {}
    current_file = None
    
    with open(dep_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("File: "):
                current_file = line.replace("File: ", "")
                deps[current_file] = []
            elif line.startswith("Calls: "):
                deps[current_file].append(line.replace("Calls: ", ""))
    
    return deps

def create_prompt(java_content, cs_skeleton, dependencies):
    system_message = """You are a code translator that helps translate Java code to C#. 
Your task is to fill in the implementation details in a C# skeleton code based on a Java implementation.

Requirements:
1. Keep all existing C# method signatures and class structure exactly the same
2. Only add implementation details inside methods
3. Maintain the same logic and behavior as the Java code
4. Follow C# conventions and best practices
5. DO NOT change any existing C# method signatures or class structure

Important dependency information:
The Java code has the following method calls and their definitions:
{dependency_info}

Please note:
- For calls marked as 'Defined in: Unknown', find appropriate C# built-in alternatives
- For calls with specific Java file definitions, you can directly use their C# counterparts as they will be available in the project
- Your response should be in pure text format, don't add any explanations besides code, don't use markdown, give pure textual code.
"""

    dependency_str = "\n".join([f"- {dep}" for dep in dependencies])

    system_message = system_message.format(dependency_info=dependency_str)

    user_message = f"""Please fill in the implementation details in the C# skeleton based on this Java implementation:

Java implementation:
{java_content}

C# skeleton (keep all signatures unchanged):
{cs_skeleton}"""

    return system_message, user_message

def call_llm(system_message, user_message):
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
    
    response = get_chat_completion(
        engine="gpt-4o-20240513",
        messages=chat_message,
    )
    
    return response.choices[0].message.content

def find_cs_skeleton(java_file_path, cs_root, project_root):
    relative_path = java_file_path.relative_to(project_root)
    cs_path = cs_root / relative_path.parent / (relative_path.stem + ".cs")
    return cs_path

def process_project(java_root, cs_root, output_root, dependency_root, project_name):
    output_root.mkdir(parents=True, exist_ok=True)
    dependency_root.mkdir(parents=True, exist_ok=True)
    
    # generate dependency file
    analyzer = DependencyAnalyzer()
    dependency_file = dependency_root / f"{project_name}_dependency_analysis.txt"
    analyzer.analyze_project(java_root, dependency_file)
    
    for java_path in java_root.rglob('*'):
        if not java_path.is_file():
            continue
            
        relative_path = java_path.relative_to(java_root)
        output_path = output_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if java_path.suffix.lower() == '.java':
            cs_path = find_cs_skeleton(java_path, cs_root, java_root)
            if cs_path and cs_path.exists():
                print(f"Processing: {java_path}")
                
                try:
                    file_deps = get_file_dependencies(dependency_root, project_name, java_path.name)
                    
                    with open(java_path, 'r', encoding='utf-8') as f:
                        java_content = f.read()
                    with open(cs_path, 'r', encoding='utf-8') as f:
                        cs_skeleton = f.read()
                    
                    system_message, user_message = create_prompt(java_content, cs_skeleton, file_deps)
                    llm_response = call_llm(system_message, user_message)
                    
                    output_path = output_root / relative_path.parent / (relative_path.stem + '.cs')
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(llm_response)
                        
                    print(f"Successfully processed: {java_path}")
                    
                except Exception as e:
                    print(f"Error processing {java_path}: {str(e)}")
            else:
                print(f"Warning: No matching C# skeleton found for {java_path}")
                
        else:
            shutil.copy2(java_path, output_path)
            print(f"Copied non-Java file: {java_path}")

def main():
    parser = argparse.ArgumentParser(description='java2csharp baseline translator with dependency analysis')
    parser.add_argument('--input-path', required=True, help='Path to Java source directory')
    parser.add_argument('--skeleton-path', required=True, help='Path to C# project skeleton')
    parser.add_argument('--output-path', required=True, help='Path for C# output')
    parser.add_argument('--dependency-path', required=True, help='Path to dependency analysis files')
    
    args = parser.parse_args()
    
    global java_root
    java_root = Path(args.input_path)
    cs_root = Path(args.skeleton_path)
    output_root = Path(args.output_path)
    dependency_path = Path(args.dependency_path)
    
    if not java_root.exists():
        raise ValueError(f"Java root path does not exist: {java_root}")
    if not cs_root.exists():
        raise ValueError(f"C# root path does not exist: {cs_root}")
    if not dependency_path.exists():
        raise ValueError(f"Dependency path does not exist: {dependency_path}")
        
    print(f"Starting translation process...")
    print(f"Java root: {java_root}")
    print(f"C# root: {cs_root}")
    print(f"Output root: {output_root}")
    print(f"Dependency path: {dependency_path}")
    
    for project in java_root.iterdir():
        if project.is_dir():
            cs_project = cs_root / project.name
            output_project = output_root / project.name
            
            if cs_project.exists():
                print(f"\nProcessing project: {project.name}")
                process_project(project, cs_project, output_project, dependency_path, project.name)
            else:
                print(f"\nWarning: No matching C# project found for {project.name}")
    
    print("\nTranslation process completed!")

if __name__ == "__main__":
    main()