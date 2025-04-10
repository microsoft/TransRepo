import os
import json
from datetime import datetime
from collections import defaultdict

def load_original_test_results(project_path):
    """Load original test results"""
    result_path = os.path.join(project_path, "test_results.json")
    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            return json.load(f)["test_results"]
    except Exception as e:
        print(f"Error loading original test results from {result_path}: {e}")
        return None

def load_iteration_results(project_path, iteration):
    """Load iteration test results"""
    result_path = os.path.join(project_path, f"test_iteration_{iteration}", "test_scores.json")
    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading iteration results from {result_path}: {e}")
        return None

def analyze_project_results(original_results, iteration_results):
    """Analyze test result comparison for a single project"""
    if not original_results or not iteration_results:
        return None

    analysis = {
        "passed_to_failed": [],  # Tests that previously passed but now fail
        "failed_to_passed": [],  # Tests that previously failed but now pass
        "total_tests": 0,
        "passed_tests": 0
    }

    individual_scores = iteration_results.get("individual_scores", {})
    
    # Analyze each test case
    for category, original_result in original_results.items():
        original_passed = original_result.get("passed", False)
        
        # Find corresponding test in iteration results
        iteration_result = individual_scores.get(category)
        if iteration_result:
            iteration_passed = (iteration_result.get("test_status") == "success" and 
                              iteration_result.get("build_status") == "success")
            
            analysis["total_tests"] += 1
            if iteration_passed:
                analysis["passed_tests"] += 1
                
            if original_passed and not iteration_passed:
                analysis["passed_to_failed"].append(category)
            elif not original_passed and iteration_passed:
                analysis["failed_to_passed"].append(category)

    return analysis

def analyze_all_projects(base_path_original, base_path_iterations):
    """Analyze test results for all projects"""
    iteration_results = {
        1: defaultdict(lambda: {"total_tests": 0, "passed_tests": 0, "passed_to_failed": [], "failed_to_passed": []}),
        2: defaultdict(lambda: {"total_tests": 0, "passed_tests": 0, "passed_to_failed": [], "failed_to_passed": []}),
        3: defaultdict(lambda: {"total_tests": 0, "passed_tests": 0, "passed_to_failed": [], "failed_to_passed": []})
    }

    # Iterate through original project directories
    for project in os.listdir(base_path_original):
        original_project_path = os.path.join(base_path_original, project)
        iteration_project_path = os.path.join(base_path_iterations, project)
        
        if not os.path.isdir(original_project_path):
            continue

        # Load original test results
        original_results = load_original_test_results(original_project_path)
        if not original_results:
            continue

        # Analyze results for each iteration
        for iteration in range(1, 4):
            iteration_result = load_iteration_results(iteration_project_path, iteration)
            if iteration_result:
                analysis = analyze_project_results(original_results, iteration_result)
                if analysis:
                    # Update statistics
                    iteration_results[iteration]["total"]["total_tests"] += analysis["total_tests"]
                    iteration_results[iteration]["total"]["passed_tests"] += analysis["passed_tests"]
                    iteration_results[iteration]["total"]["passed_to_failed"].extend(
                        [f"{project}:{test}" for test in analysis["passed_to_failed"]])
                    iteration_results[iteration]["total"]["failed_to_passed"].extend(
                        [f"{project}:{test}" for test in analysis["failed_to_passed"]])
                    
                    # Save analysis results for individual project
                    iteration_results[iteration][project] = {
                        "total_tests": analysis["total_tests"],
                        "passed_tests": analysis["passed_tests"],
                        "passed_to_failed": analysis["passed_to_failed"],
                        "failed_to_passed": analysis["failed_to_passed"]
                    }

    return iteration_results

def save_analysis_results(results, base_path_iterations):
    """Save analysis results"""
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "iterations": {}
    }

    for iteration, data in results.items():
        total_data = data["total"]
        success_rate = (total_data["passed_tests"] / total_data["total_tests"] * 100 
                       if total_data["total_tests"] > 0 else 0)
        
        output_data["iterations"][f"iteration_{iteration}"] = {
            "summary": {
                "total_tests": total_data["total_tests"],
                "passed_tests": total_data["passed_tests"],
                "success_rate": round(success_rate, 2),
                "passed_to_failed_count": len(total_data["passed_to_failed"]),
                "failed_to_passed_count": len(total_data["failed_to_passed"])
            },
            "passed_to_failed": total_data["passed_to_failed"],
            "failed_to_passed": total_data["failed_to_passed"],
            "project_details": {
                project: details for project, details in data.items() 
                if project != "total"
            }
        }

    output_path = os.path.join(base_path_iterations, "test_analysis_results.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"Analysis results saved to: {output_path}")
    except Exception as e:
        print(f"Error saving analysis results: {e}")

def main():
    base_path_original = ""
    base_path_iterations = ""
    
    results = analyze_all_projects(base_path_original, base_path_iterations)
    save_analysis_results(results, base_path_iterations)

if __name__ == "__main__":
    main()