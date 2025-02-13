import os
import json

def analyze_dependencies(base_path, output_path):
    # 初始化结果字典
    results = {
        'overall_stats': {},
        'project_stats': {},
        'missing_functions': []
    }
    
    # 统计变量
    all_missing_functions = set()
    total_tests = 0
    total_failed_tests = 0
    
    for project in os.listdir(base_path):
        project_path = os.path.join(base_path, project)
        if not os.path.isdir(project_path):
            continue
            
        # 只查找test_iteration_3
        iteration_path = os.path.join(project_path, 'test_iteration_3')
        if not os.path.exists(iteration_path):
            continue
            
        json_path = os.path.join(iteration_path, 'missing_dependencies.json')
        if not os.path.exists(json_path):
            continue
        
        # 初始化项目统计
        project_stats = {
            'total_tests': 0,
            'failed_tests': 0,
            'failure_percentage': 0.0
        }
        
        # 计算项目的test数量
        project_total_tests = sum(1 for item in os.listdir(iteration_path) 
                                if os.path.isdir(os.path.join(iteration_path, item)))
        project_stats['total_tests'] = project_total_tests
        total_tests += project_total_tests
        
        # 解析json文件
        with open(json_path, 'r') as f:
            content = f.read()
            # 处理多个json对象连接在一起的情况
            json_objects = content.split('}{')
            for i, obj in enumerate(json_objects):
                if i > 0:
                    obj = '{' + obj
                if i < len(json_objects) - 1:
                    obj = obj + '}'
                
                try:
                    data = json.loads(obj)
                    missing_deps = data.get('missing_dependencies', [])
                    if missing_deps:  # 如果有缺失的依赖
                        project_stats['failed_tests'] += 1
                        total_failed_tests += 1
                        # 收集所有缺失的函数
                        for dep in missing_deps:
                            func_info = {
                                'file': dep['file'],
                                'function': dep['function'],
                                'parameter_types': dep['parameter_types']
                            }
                            func_key = (dep['file'], dep['function'], dep['parameter_types'])
                            if func_key not in all_missing_functions:
                                all_missing_functions.add(func_key)
                                results['missing_functions'].append(func_info)
                except json.JSONDecodeError:
                    print(f"Error parsing JSON in {json_path}")
                    continue
        
        # 计算项目的失败率
        project_stats['failure_percentage'] = round(
            (project_stats['failed_tests'] / project_stats['total_tests'] * 100) 
            if project_stats['total_tests'] > 0 else 0, 2
        )
        
        # 保存项目统计
        results['project_stats'][project] = project_stats

    # 计算总体统计数据
    overall_percentage = (total_failed_tests / total_tests * 100) if total_tests > 0 else 0
    
    results['overall_stats'] = {
        'total_tests': total_tests,
        'missing_dependency_tests': total_failed_tests,
        'missing_percentage': round(overall_percentage, 2),
        'unique_missing_functions_count': len(all_missing_functions)
    }

    # 保存结果到json文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    # 打印简要统计结果
    print("\nAnalysis completed!")
    print(f"Results have been saved to: {output_path}")
    print(f"\nOverall summary:")
    print(f"Total tests: {total_tests}")
    print(f"Missing Dependency tests: {total_failed_tests}")
    print(f"Overall Missing percentage: {overall_percentage:.2f}%")
    print(f"Unique missing functions: {len(all_missing_functions)}")
    print("\nProject-wise summary:")
    for project, stats in results['project_stats'].items():
        print(f"\n{project}:")
        print(f"Total tests: {stats['total_tests']}")
        print(f"Missing Dependency tests: {stats['failed_tests']}")
        print(f"Missing percentage: {stats['failure_percentage']}%")

if __name__ == "__main__":
    base_path = ""
    output_path = base_path + "/missing_dependency.json"
    analyze_dependencies(base_path, output_path)