import os
import json
import shutil
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from alive_progress import alive_bar, config_handler
from verify.test_scoring import TestScoring
from verify.func_replacer import FunctionReplacer

class ParserError(Exception):
    """Custom exception for parser-related errors"""
    pass

def save_results(results, output_base_path):
    """
    Save test results to a JSON file
    Args:
        results: Test execution results
        output_base_path: Base directory for output files
    Returns:
        str: Path to the saved results file
    """
    results_dir = os.path.join(output_base_path, 'test_results')
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = os.path.join(results_dir, f'test_results_{timestamp}.json')
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"[INFO] Results saved to: {result_file}")
    return result_file

def handle_tree_sitter_error(error, file_path):
    """
    Handle tree-sitter related errors
    Args:
        error: The caught exception
        file_path: Path to the file being processed
    Returns:
        dict: Error information
    """
    error_msg = str(error)
    if "object has no attribute 'query'" in error_msg:
        return {
            'error_type': 'TreeSitterQueryError',
            'message': f"Tree-sitter parser query initialization failed for file: {file_path}",
            'details': error_msg,
            'recommendation': "Ensure tree-sitter is properly installed and initialized"
        }
    return {
        'error_type': 'UnknownParserError',
        'message': f"Unknown parser error occurred while processing file: {file_path}",
        'details': error_msg
    }

def copy_skeleton_and_run_test(skeleton_path, translated_path, json_path, output_base_path):
    """
    Main function to copy skeleton code and execute tests
    Args:
        skeleton_path: Path to skeleton code
        translated_path: Path to translated code
        json_path: Path to test configuration JSON
        output_base_path: Base directory for test outputs
    Returns:
        dict: Test execution results
    """
    print("[DEBUG] Starting test execution process...")
    
    replacer = FunctionReplacer()
    results = {}
    
    try:
        with open(json_path, 'r') as f:
            test_configs = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON configuration: {str(e)}")
        return {'error': f"JSON parsing error: {str(e)}"}
    except FileNotFoundError:
        print(f"[ERROR] JSON configuration file not found: {json_path}")
        return {'error': f"Configuration file not found: {json_path}"}
    
    scorer = TestScoring()
    
    # Rest of the function remains the same, just with English comments
    # ... (Previous implementation)

def main():
    """Main entry point of the test execution framework"""
    print("[DEBUG] Initializing test execution framework...")
    
    # Configure paths using relative paths
    base_dir = Path(__file__).parent.parent  # Adjust according to your project structure
    skeleton_path = base_dir / "output/skeleton/c_sharp/hutool_succ/hutool-script"
    translated_path = base_dir / "output/java2csharp/baseline_one2one/hutool-script"
    json_path = base_dir / "output/dependency/hutool-script/test_dependency.json"
    output_base_path = base_dir / "output/java2csharp/validation/test-script"
    
    print("[DEBUG] Configuration:")
    print(f"[DEBUG] Skeleton Path: {skeleton_path}")
    print(f"[DEBUG] Translated Path: {translated_path}")
    print(f"[DEBUG] JSON Path: {json_path}")
    print(f"[DEBUG] Output Base Path: {output_base_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_base_path, exist_ok=True)
    print("[DEBUG] Created output base directory")
    
    # Configure progress bar settings
    config_handler.set_global(
        length=40,
        spinner='stars',
        bar='circles'
    )
    print("[DEBUG] Progress bar configuration set")
    
    print("\n[INFO] Starting test execution...")
    
    # Execute tests
    results = copy_skeleton_and_run_test(
        str(skeleton_path),
        str(translated_path),
        str(json_path),
        str(output_base_path)
    )
    
    # Save and display results
    result_file = save_results(results, str(output_base_path))
    
    # Display test summary
    print("\n[INFO] Test Results Summary:")
    print("=" * 50)
    
    total_score = 0
    test_count = 0
    
    for test_name, result in results.items():
        print(f"\nTest: {test_name}")
        if 'error' in result:
            print(f"[ERROR] Error occurred: {result['error']}")
            print(f"[SCORE] 0/100")
        else:
            print(f"[INFO] Build Status: {result['build']}")
            print(f"[INFO] Build Score: {result['build_score']}/30")
            
            if result['build'] == 'success':
                print(f"[INFO] Test Status: {result['test']}")
                print(f"[INFO] Test Score: {result['test_score']}/70")
            
            print(f"[SCORE] Total Score: {result['total_score']}/100")
            
            total_score += result['total_score']
            test_count += 1
    
    if test_count > 0:
        average_score = total_score / test_count
        print(f"\n[FINAL] Average Score Across All Tests: {average_score:.2f}/100")
        print(f"[INFO] Detailed results saved to: {result_file}")

if __name__ == "__main__":
    main()