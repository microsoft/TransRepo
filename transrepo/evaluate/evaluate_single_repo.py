import os
import json
from typing import Dict, Tuple, List
import pandas as pd

def read_test_scores(file_path: str) -> Tuple[float, float]:
    """
    Read test_scores.json and return build rate and test rate
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Calculate build rate
        build_success = sum(1 for test in data['individual_scores'].values() 
                          if test['build_status'] == 'success')
        total_tests = len(data['individual_scores'])
        build_rate = (build_success / total_tests) * 100 if total_tests > 0 else 0
        
        # Get test rate from summary
        test_rate = data['summary']['success_rate']
        
        return build_rate, test_rate
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return 0.0, 0.0

def analyze_project(project_path: str) -> Tuple[float, float]:
    """
    Analyze a project directory and return the highest build rate and test rate across iterations
    """
    max_build_rate = 0.0
    max_test_rate = 0.0
    
    for i in range(1, 4):  # iterations 1-3
        iteration_dir = f"test_iteration_{i}"
        scores_path = os.path.join(project_path, iteration_dir, "test_scores.json")
        
        if os.path.exists(scores_path):
            build_rate, test_rate = read_test_scores(scores_path)
            max_build_rate = max(max_build_rate, build_rate)
            max_test_rate = max(max_test_rate, test_rate)
    
    return max_build_rate, max_test_rate

def analyze_llm_results(paths: List[str]) -> pd.DataFrame:
    """
    Analyze results for multiple LLMs and return a DataFrame with the results
    """
    results = []
    
    for path in paths:
        llm_name = os.path.basename(path)
        
        # Iterate through all project directories
        for project_dir in os.listdir(path):
            project_path = os.path.join(path, project_dir)
            if os.path.isdir(project_path):
                max_build_rate, max_test_rate = analyze_project(project_path)
                results.append({
                    'LLM': llm_name,
                    'Project': project_dir,
                    'Max Build Rate': max_build_rate,
                    'Max Test Rate': max_test_rate
                })
    
    # Create DataFrame and calculate averages
    df = pd.DataFrame(results)
    if not df.empty:
        avg_row = {
            'LLM': 'Average',
            'Project': '',
            'Max Build Rate': df['Max Build Rate'].mean(),
            'Max Test Rate': df['Max Test Rate'].mean()
        }
        df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)
    
    return df

def main():
    # Get input paths from user
    paths = []
    while True:
        path = input("Enter path for LLM (or press Enter to finish): ").strip()
        if not path:
            break
        if os.path.exists(path):
            paths.append(path)
        else:
            print(f"Path {path} does not exist!")
    
    if not paths:
        print("No valid paths provided!")
        return
    
    # Analyze results and create DataFrame
    results_df = analyze_llm_results(paths)
    
    # Display results
    pd.set_option('display.float_format', '{:.2f}'.format)
    print("\nResults:")
    print(results_df)
    
    # Save results to CSV
    output_file = "llm_analysis_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()