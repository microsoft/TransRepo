import os
import json
from collections import defaultdict

def analyze_test_results(path):
    # Directly get all folders under path as projects
    projects = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    iterations = {}
    
    # Analyze results for each project
    for project in projects:
        history_path = os.path.join(path, project, 'optimization_history.json')
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                history = json.load(f)
                
                # Analyze each iteration
                for entry in history:
                    iteration = entry['iteration']
                    if iteration not in iterations:
                        iterations[iteration] = {
                            'error_types': defaultdict(set),  # Record all error types
                            'project_distribution': defaultdict(dict)  # Record error distribution for each project
                        }
                    
                    # Analyze results for each test case
                    test_results = entry['test_results']
                    project_errors = defaultdict(set)  # Error set for this project
                    
                    for test_name, result in test_results.items():
                        # Check for compilation errors
                        if result['build'] == 'failed':
                            build_output = result['build_output']
                            for line in build_output.split('\n'):
                                if 'error CS' in line:
                                    error_code = line.split('error ')[1].split(':')[0]
                                    error_type = f"compiling_error_{error_code}"
                                    iterations[iteration]['error_types'][error_type].add(test_name)
                                    project_errors[error_type].add(test_name)
                        
                        # Check for runtime errors and functional errors
                        elif result['build'] == 'success':
                            if result['test_score'] == 0:
                                if 'assertion failed' in result.get('test_output', '').lower():
                                    error_type = 'functional_error_assertion'
                                    iterations[iteration]['error_types'][error_type].add(test_name)
                                    project_errors[error_type].add(test_name)
                                else:
                                    error_type = 'runtime_error_unknown'
                                    iterations[iteration]['error_types'][error_type].add(test_name)
                                    project_errors[error_type].add(test_name)
                    
                    # Record error distribution for this project
                    for error_type, test_cases in project_errors.items():
                        iterations[iteration]['project_distribution'][project][error_type] = list(test_cases)
    
    # Generate summary results
    summary = {
        'summary': [{
            'iteration': iter_num,
            'error_types': {
                error_type: len(test_cases)
                for error_type, test_cases in data['error_types'].items()
            },
            'project_distribution': data['project_distribution']
        } for iter_num, data in iterations.items()]
    }
    
    # Write results to file
    output_path = os.path.join(path, 'error_analysis.json')
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    return summary

def main():
    path = "enter your root path here"
        
    try:
        result = analyze_test_results(path)
        print("Analysis complete. Results written to error_analysis.json")
        print("\nSummary:")
        for iteration in result['summary']:
            print(f"\nIteration {iteration['iteration']}:")
            print("Error types:")
            for error_type, count in iteration['error_types'].items():
                print(f"  {error_type}: {count}")
            print("Project distribution:")
            for project, errors in iteration['project_distribution'].items():
                print(f"  {project}:")
                for error_type, test_cases in errors.items():
                    print(f"    {error_type}: {len(test_cases)} test cases")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()