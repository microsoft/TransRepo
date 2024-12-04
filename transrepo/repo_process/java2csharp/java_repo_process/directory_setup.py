import os

def create_directory_structure(project_path):
    """Create standard Maven project structure"""
    directories = [
        os.path.join('repo_process', 'main', 'java'),
        os.path.join('repo_process', 'main', 'resources'),
        os.path.join('repo_process', 'test', 'java'),
        os.path.join('repo_process', 'test', 'resources')
    ]
    
    for directory in directories:
        full_path = os.path.join(project_path, directory)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")