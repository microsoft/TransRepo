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
    """Same as original implementation"""
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

def copy_skeleton_and_run_test(
    skeleton_path, 
    translated_path, 
    json_path, 
    output_base_path
):
    """
    处理单个库的复制、依赖替换、编译、测试流程
    """
    print(f"[DEBUG] Starting test execution process for:\n"
          f"Skeleton Path: {skeleton_path}\n"
          f"Translated Path: {translated_path}\n"
          f"JSON Path: {json_path}\n"
          f"Output Base Path: {output_base_path}")

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
    
    # 拼出 missing_dependencies 的路径
    missing_dependencies_path = os.path.join(output_base_path, "missing_dependencies.json")

    # 取测试列表
    tests = test_configs.get('tests', [])
    if not tests:
        print("[WARN] No tests found in JSON.")
        return {}

    with alive_bar(len(tests), spinner='stars', title='Running tests') as bar:
        for test_case in tests:
            test_info = test_case['test']
            test_name = test_info['testname']
            dependencies = test_case['dependencies']
            
            print(f"\n[DEBUG] Processing test: {test_name}")
            
            test_output_dir = os.path.join(output_base_path, f"test_{test_name}")
            os.makedirs(test_output_dir, exist_ok=True)
            
            try:
                # 复制 skeleton 目录
                shutil.copytree(skeleton_path, test_output_dir, dirs_exist_ok=True)
                
                # 处理依赖
                try:
                    replacer.process_test_dependencies(
                        translated_path,
                        test_output_dir,
                        dependencies,
                        missing_dependencies_path  # 传入missing_dependencies
                    )
                except AttributeError as e:
                    error_info = handle_tree_sitter_error(e, translated_path)
                    results[test_name] = {
                        'error': error_info,
                        'build_score': 0,
                        'test_score': 0,
                        'total_score': 0
                    }
                    bar()
                    continue
                
                # dotnet build
                build_result = subprocess.run(
                    ['dotnet', 'build'],
                    cwd=test_output_dir,
                    capture_output=True,
                    text=True
                )
                
                if build_result.returncode == 0:
                    # dotnet test
                    test_result = subprocess.run(
                        ['dotnet', 'test', '--filter', f"Category={test_name}"],
                        cwd=test_output_dir,
                        capture_output=True,
                        text=True
                    )
                    
                    test_status = 'success' if test_result.returncode == 0 else 'failed'
                    
                    test_data = {
                        'build': 'success',
                        'test': test_status,
                        'test_output': test_result.stdout,
                        'build_output': build_result.stdout,
                        'test_error': test_result.stderr
                    }
                    
                    score_results = scorer.calculate_final_score(test_data)
                    results[test_name] = {**test_data, **score_results}
                    print(f"Score for {test_name} is {score_results}")
                    
                else:
                    results[test_name] = {
                        'build': 'failed',
                        'build_error': build_result.stderr,
                        'build_output': build_result.stdout,
                        'build_score': 0,
                        'test_score': 0,
                        'total_score': 0
                    }
                    
            except Exception as e:
                print(f"[ERROR] Exception in test {test_name}: {str(e)}")
                print(f"[ERROR] Traceback: {traceback.format_exc()}")
                results[test_name] = {
                    'error': {
                        'message': str(e),
                        'traceback': traceback.format_exc()
                    },
                    'build_score': 0,
                    'test_score': 0,
                    'total_score': 0
                }
            
            bar()
    
    # ======= 生成总结分数 =======

    total_score = 0
    test_count = len(results)
    successful_tests = 0
    score_summary = {
        'individual_scores': {},
        'summary': {
            'total_score': 0,
            'average_score': 0,
            'test_count': test_count,
            'successful_tests': 0,
            'success_rate': 0
        }
    }

    for test_name, result in results.items():
        test_score = result.get('total_score', 0)
        total_score += test_score
        score_summary['individual_scores'][test_name] = {
            'total_score': test_score,
            'build_score': result.get('build_score', 0),
            'test_score': result.get('test_score', 0),
            'build_status': result.get('build', 'failed'),
            'test_status': result.get('test', 'failed')
        }
        
        if result.get('build') == 'success' and result.get('test') == 'success':
            successful_tests += 1

    score_summary['summary']['total_score'] = total_score
    score_summary['summary']['average_score'] = total_score / test_count if test_count > 0 else 0
    score_summary['summary']['successful_tests'] = successful_tests
    score_summary['summary']['success_rate'] = (successful_tests / test_count * 100) if test_count > 0 else 0

    # 保存详细结果
    detailed_results_path = os.path.join(output_base_path, 'test_results_detailed.json')
    with open(detailed_results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # 保存分数总结
    score_summary_path = os.path.join(output_base_path, 'test_scores.json')
    with open(score_summary_path, 'w', encoding='utf-8') as f:
        json.dump(score_summary, f, indent=2, ensure_ascii=False)

    print(f"\n[INFO] Test results saved to: {detailed_results_path}")
    print(f"[INFO] Score summary saved to: {score_summary_path}")

    # 返回本库的所有结果
    return results


def run_tests_for_library(
    library_name,
    parent_skeleton_path,
    parent_translated_path,
    parent_json_path,
    parent_output_path
):
    """
    处理单个库的入口
    """
    skeleton_path = os.path.join(parent_skeleton_path, library_name)
    translated_path = os.path.join(parent_translated_path, library_name)
    # JSON 文件名称与库名对应
    json_path = os.path.join(parent_json_path, f"{library_name}.json")
    output_base_path = os.path.join(parent_output_path, library_name)
    
    print("\n" + "=" * 60)
    print(f"[INFO] Now processing library: {library_name}")
    print("=" * 60)
    
    # 创建库的 output 根目录
    os.makedirs(output_base_path, exist_ok=True)

    # 如果对应的 JSON 文件不存在，就跳过
    if not os.path.isfile(json_path):
        print(f"[WARN] No JSON file found for {library_name}, skipping...")
        return {}
    
    # 调用处理逻辑
    results = copy_skeleton_and_run_test(
        skeleton_path,
        translated_path,
        json_path,
        output_base_path
    )
    
    # 将结果另存
    result_file = save_results(results, output_base_path)
    
    print("\n[INFO] Test Results Summary for", library_name)
    print("=" * 50)
    
    total_score = 0
    test_count = 0

    # 打印结果
    if isinstance(results, dict):
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

    return results


def main():
    """
    遍历 parent_skeleton_path 下所有子目录(库)，依次处理
    """
    print("[DEBUG] Initializing test execution framework...")

    # 设置四个父路径
    parent_skeleton_path = "/home/v-zhangxing/TransRepo-Data/data/c_sharp_skeleton"
    parent_translated_path = "/home/v-zhangxing/TransRepo-Data/data/c_sharp_skeleton"
    parent_json_path = "/home/v-zhangxing/TransRepo-Data/data/test_dependency/fixed_v2"
    parent_output_path = "/home/v-zhangxing/test_output"
    
    # 设置进度条风格（全局）
    config_handler.set_global(
        length=40,
        spinner='stars',
        bar='circles'
    )

    # 获取 parent_skeleton_path 下的所有子目录（即库名）
    all_dirs = [
        d for d in os.listdir(parent_skeleton_path)
        if os.path.isdir(os.path.join(parent_skeleton_path, d))
           and not d.startswith('.')  # 可选：排除隐藏文件夹
    ]

    # 遍历所有库目录
    for library_name in all_dirs:
        run_tests_for_library(
            library_name,
            parent_skeleton_path,
            parent_translated_path,
            parent_json_path,
            parent_output_path
        )

if __name__ == "__main__":
    main()
