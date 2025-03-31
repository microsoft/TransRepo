import os
import json
from collections import defaultdict
from datetime import datetime

def analyze_test_results(base_path, output_filename="test_analysis_results.json"):
    stats = defaultdict(lambda: {"total_test_count": 0, "total_successful_tests": 0})
    
    for project in os.listdir(base_path):
        project_path = os.path.join(base_path, project)
        if not os.path.isdir(project_path):
            continue
        for i in range(1, 4): 
            iteration_folder = f"test_iteration_{i}"
            scores_path = os.path.join(project_path, iteration_folder, "test_scores.json")

            if not os.path.exists(scores_path):
                continue
            print("iteration found")
            try:
                with open(scores_path, 'r') as f:
                    data = json.load(f)
                    summary = data.get("summary", {})
                    
                    # Accumulate statistics
                    stats[iteration_folder]["total_test_count"] += summary.get("test_count", 0)
                    stats[iteration_folder]["total_successful_tests"] += summary.get("successful_tests", 0)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading {scores_path}: {e}")
    
    # Calculate success rate and format output data
    output_data = {
        "analysis_timestamp": datetime.now().isoformat(),
        "results": {}
    }
    
    for iteration, data in sorted(stats.items()):
        total_tests = data["total_test_count"]
        successful_tests = data["total_successful_tests"]
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        output_data["results"][iteration] = {
            "total_test_count": total_tests,
            "total_successful_tests": successful_tests,
            "success_rate": round(success_rate, 2)
        }
    
    # Save results to JSON file
    output_path = os.path.join(base_path, output_filename)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults have been saved to: {output_path}")
        
        # Print statistical results
        print("\n=== Test Results Analysis ===")
        for iteration, data in output_data["results"].items():
            print(f"\n{iteration}:")
            print(f"Total test count: {data['total_test_count']}")
            print(f"Total successful tests: {data['total_successful_tests']}")
            print(f"Overall success rate: {data['success_rate']}%")
            
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")

if __name__ == "__main__":
    base_path = ""
    analyze_test_results(base_path)