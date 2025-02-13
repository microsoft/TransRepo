import os
import json
from collections import defaultdict

def analyze_test_scores(base_path):
    statistics = {
        "test_iteration_1": {"total": 0, "success": 0, "success_rate": 0},
        "test_iteration_2": {"total": 0, "success": 0, "success_rate": 0}, 
        "test_iteration_3": {"total": 0, "success": 0, "success_rate": 0}
    }
    
    for project in os.listdir(base_path):
        project_path = os.path.join(base_path, project)
        if not os.path.isdir(project_path):
            continue
            
        for iteration in ["test_iteration_1", "test_iteration_2", "test_iteration_3"]:
            iteration_path = os.path.join(project_path, iteration)
            if not os.path.exists(iteration_path):
                continue
                
            scores_file = os.path.join(iteration_path, "test_scores.json")
            if not os.path.exists(scores_file):
                continue
                
            try:
                with open(scores_file, 'r') as f:
                    scores_data = json.load(f)
                
                for test_case in scores_data["individual_scores"].values():
                    statistics[iteration]["total"] += 1
                    if test_case["build_status"] == "success":
                        statistics[iteration]["success"] += 1
                        
            except Exception as e:
                print(f"Error processing {scores_file}: {str(e)}")
                
    for iteration_stats in statistics.values():
        if iteration_stats["total"] > 0:
            iteration_stats["success_rate"] = round(iteration_stats["success"] / iteration_stats["total"] * 100, 2)
            
    output_file = os.path.join(base_path, "build_statistics.json")
    with open(output_file, 'w') as f:
        json.dump(statistics, f, indent=2)
        
    return statistics

if __name__ == "__main__":
        
    path = "enter your root path here"

        
    results = analyze_test_scores(path)
    print("Statistics saved to build_statistics.json")
    print("Results:")
    print(json.dumps(results, indent=2))