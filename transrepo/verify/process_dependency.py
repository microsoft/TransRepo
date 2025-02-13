import json
import ast
import os

def convert_path_to_src_relative(path):
    # Find the last occurrence of 'src' in the path
    if 'src' in path:
        src_index = path.find('/src/')
        if src_index != -1:
            # Return the path starting from 'src'
            return 'src' + path[src_index + 4:]
    return path

def convert_jsonl_to_json(input_file, output_file):
    # Read all lines
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    result = []
    current_test = None
    current_dependencies = []
    
    for line in lines:
        try:
            # Use ast.literal_eval to handle dictionaries with single quotes
            data = ast.literal_eval(line.strip())
            
            # Process file paths, convert to src-relative paths
            if 'file' in data:
                data['file'] = convert_path_to_src_relative(data['file'])
            
            # If it's a test case (contains testname field)
            if 'testname' in data:
                # If there's already a test case, save the current group
                if current_test:
                    result.append({
                        "test": current_test,
                        "dependencies": current_dependencies
                    })
                
                # Start a new test case
                current_test = data
                current_dependencies = []
            else:
                # Add to current dependencies list, use dictionary to deduplicate
                dep_key = (data.get('source_function'), data.get('sourceClass'))
                if dep_key not in [(d.get('source_function'), d.get('sourceClass')) for d in current_dependencies]:
                    current_dependencies.append(data)
                
        except (SyntaxError, ValueError) as e:
            # If this line is incomplete or malformed, try to fix and parse
            try:
                # Check if it's truncated and missing closing quotes and braces
                if line.strip().endswith("'"):
                    line = line.strip() + "'"
                if not line.strip().endswith("}"):
                    line = line.strip() + "}"
                data = ast.literal_eval(line.strip())
                
                if 'file' in data:
                    data['file'] = convert_path_to_src_relative(data['file'])
                
                if 'testname' in data:
                    if current_test:
                        result.append({
                            "test": current_test,
                            "dependencies": current_dependencies
                        })
                    current_test = data
                    current_dependencies = []
                else:
                    dep_key = (data.get('source_function'), data.get('sourceClass'))
                    if dep_key not in [(d.get('source_function'), d.get('sourceClass')) for d in current_dependencies]:
                        current_dependencies.append(data)
                        
            except Exception as e2:
                print(f"Warning: Could not parse line after fix attempt: {line}")
                continue
    
    # Process the last group
    if current_test:
        result.append({
            "test": current_test,
            "dependencies": current_dependencies
        })
    
    # Write the processed results
    with open(output_file, 'w') as f:
        json.dump({"tests": result}, f, indent=2)
        
if __name__ == "__main__":
    if __name__ == "__main__":
    convert_jsonl_to_json(
        'output/dependency/hutool-script/test_dependency.jsonl',
        'output/dependency/hutool-script/test_dependency.json'
    )