import os
import re

def process_test_file(file_path):
    """
    Process a single C# test file to add Category attributes
    Args:
        file_path: Path to the .cs file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regular expression to find test methods
    # Matches [Test] attribute and the following method declaration
    pattern = r'(\s*)\[Test\](\s*)(public\s+void\s+(\w+)\s*\([^)]*\))'

    # Function to replace matched pattern
    def add_category(match):
        indent = match.group(1)          # Preserve indentation
        test_attr = match.group(2)       # Preserve spacing after [Test]
        method_decl = match.group(3)     # Method declaration
        method_name = match.group(4)     # Method name
        
        # Check if Category already exists
        category_pattern = rf'\[Category\("{method_name}"\)\]'
        if re.search(category_pattern, content):
            return f"{indent}[Test]{test_attr}{method_decl}"
            
        return f"{indent}[Test]{test_attr}{indent}[Category(\"{method_name}\")]{test_attr}{method_decl}"

    # Replace in content
    modified_content = re.sub(pattern, add_category, content)

    # Only write if content has changed
    if modified_content != content:
        print(f"Modifying: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    else:
        print(f"No changes needed in: {file_path}")

def find_test_files(root_dir):
    """
    Find all .cs files in src/test directory and its subdirectories
    Args:
        root_dir: Repository root directory
    Returns:
        List of paths to .cs files
    """
    test_dir = os.path.join(root_dir, 'src', 'test')
    if not os.path.exists(test_dir):
        print(f"Test directory not found: {test_dir}")
        return []

    test_files = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.cs'):
                test_files.append(os.path.join(root, file))
    return test_files

def main():
    """
    Main function to process all test files in the repository
    """
    # Get repository root path from command line or use current directory
    import sys
    repo_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    print(f"Processing repository: {repo_root}")
    
    # Find all test files
    test_files = find_test_files(repo_root)
    print(f"Found {len(test_files)} .cs files")
    
    # Process each file
    for file_path in test_files:
        try:
            process_test_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    main()