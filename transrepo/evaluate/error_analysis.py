import os
import json
from collections import defaultdict

def analyze_test_results(path):
    # 直接获取path下的所有文件夹作为projects
    projects = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    iterations = {}
    
    # 分析每个project的结果
    for project in projects:
        history_path = os.path.join(path, project, 'optimization_history.json')
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                history = json.load(f)
                
                # 分析每个iteration
                for entry in history:
                    iteration = entry['iteration']
                    if iteration not in iterations:
                        iterations[iteration] = {
                            'error_types': defaultdict(set),  # 记录所有错误类型
                            'project_distribution': defaultdict(dict)  # 记录每个project的错误分布
                        }
                    
                    # 分析每个test case的结果
                    test_results = entry['test_results']
                    project_errors = defaultdict(set)  # 该project的错误集合
                    
                    for test_name, result in test_results.items():
                        # 检查编译错误
                        if result['build'] == 'failed':
                            build_output = result['build_output']
                            for line in build_output.split('\n'):
                                if 'error CS' in line:
                                    error_code = line.split('error ')[1].split(':')[0]
                                    error_type = f"compiling_error_{error_code}"
                                    iterations[iteration]['error_types'][error_type].add(test_name)
                                    project_errors[error_type].add(test_name)
                        
                        # 检查运行时错误和功能性错误
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
                    
                    # 记录该project的错误分布
                    for error_type, test_cases in project_errors.items():
                        iterations[iteration]['project_distribution'][project][error_type] = list(test_cases)
    
    # 生成总结结果
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
    
    # 写入结果文件
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