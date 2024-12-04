import subprocess

def run_tests(project_path):
    """Run Maven tests"""
    try:
        result = subprocess.run(['mvn', 'clean', 'test'], 
                              cwd=project_path,
                              capture_output=True,
                              text=True)
        if result.returncode != 0:
            print("Maven output:")
            print(result.stdout)
            print("Maven errors:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return False