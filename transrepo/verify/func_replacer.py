import json
import os
import shutil
import tree_sitter
from tree_sitter import Language, Parser

class FunctionReplacer:
    def __init__(self, grammar_path='./my-language.so'):
        """
        Initialize FunctionReplacer
        Args:
            grammar_path: Path to the tree-sitter grammar library
        """
        grammar_path = os.path.abspath(grammar_path)
        print(f"[DEBUG] Resolved grammar_path: {grammar_path}")

        # Build grammar library if it doesn't exist
        if not os.path.exists(grammar_path):
            os.makedirs(os.path.dirname(grammar_path), exist_ok=True)
            Language.build_library(
                grammar_path,
                [
                    './tree-sitter-java',
                    './tree-sitter-c-sharp'
                ]
            )
        
        self.JAVA_LANGUAGE = Language(grammar_path, 'java')
        self.CSHARP_LANGUAGE = Language(grammar_path, 'c_sharp')
        
        self.java_parser = Parser()
        self.java_parser.set_language(self.JAVA_LANGUAGE)

        self.csharp_parser = Parser()
        self.csharp_parser.set_language(self.CSHARP_LANGUAGE)

    def get_parameter_types(self, method_node):
        """
        Extract parameter types from a method node
        """
        parameters = []
        formal_parameters = method_node.child_by_field_name('parameters')
        if formal_parameters:
            for param in formal_parameters.children:
                if param.type == 'formal_parameter':
                    type_node = param.child_by_field_name('type')
                    if type_node:
                        parameters.append(type_node.text.decode('utf8'))
        return ','.join(parameters) if parameters else 'None'

    def replace_functions_in_file(self, source_file, output_file, dependencies):
        """
        Replace multiple functions in a file based on function name and parameter types
        """
        print(f"[Replacement DEBUG] Total functions to replace: {len(dependencies)}")

        functions_to_find = set((d['source_function'], d['parameter_types']) for d in dependencies)
        function_names_to_find = set(d['source_function'] for d in dependencies)
        
        found_in_source = set()
        found_in_output = set()
        found_complete_matches = set()

        # 用来收集函数名匹配，但参数不匹配时的一些信息（如有需要也可拓展）
        name_only_matches_in_source = {}
        name_only_matches_in_output = {}
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            with open(output_file, 'r', encoding='utf-8') as f:
                output_code = f.read()
            
            source_tree = self.java_parser.parse(bytes(source_code, 'utf8'))
            output_tree = self.java_parser.parse(bytes(output_code, 'utf8'))

            # 同时匹配方法声明 + 构造函数
            query = self.JAVA_LANGUAGE.query("""
                (method_declaration
                    name: (identifier) @method_name) @method
                (constructor_declaration
                    name: (identifier) @constructor_name) @constructor
            """)
            
            source_methods = {}
            
            # 遍历 source_file AST
            for node, capture_name in query.captures(source_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)
                    signature = (method_name, param_types)

                    # 如果 signature 在我们的待匹配列表
                    if signature in functions_to_find:
                        found_in_source.add(signature)
                    
                    # 如果仅函数名在我们的待匹配列表
                    if method_name in function_names_to_find:
                        if method_name not in name_only_matches_in_source:
                            name_only_matches_in_source[method_name] = []
                        name_only_matches_in_source[method_name].append((param_types, signature))

                    # 保存原函数（或构造函数）的代码片段
                    body = node.child_by_field_name('body')
                    if body:
                        end_byte = body.end_byte
                        while end_byte < len(source_code.encode('utf8')) and source_code.encode('utf8')[end_byte-1:end_byte] != b'}':
                            end_byte += 1
                        
                        source_methods[(method_name, param_types)] = (
                            node.start_byte,
                            end_byte,
                            source_code[node.start_byte:end_byte]
                        )
            
            # 遍历 output_file AST，用以找需要替换的位置
            modified_code = output_code
            replacements = []
            
            for node, capture_name in query.captures(output_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)
                    signature = (method_name, param_types)
                    
                    if signature in functions_to_find:
                        found_in_output.add(signature)
                    
                    if method_name in function_names_to_find:
                        if method_name not in name_only_matches_in_output:
                            name_only_matches_in_output[method_name] = []
                        name_only_matches_in_output[method_name].append((param_types, signature))
                        
                        # 如果源文件里存在该方法（signature 匹配到了），则进行替换
                        if signature in found_in_source:
                            source_method = source_methods.get(signature)
                            if source_method:
                                body = node.child_by_field_name('body')
                                if body:
                                    end_byte = body.end_byte
                                    while end_byte < len(output_code.encode('utf8')) and output_code.encode('utf8')[end_byte-1:end_byte] != b'}':
                                        end_byte += 1
                                    
                                    replacements.append((
                                        node.start_byte,
                                        end_byte,
                                        source_method[2]
                                    ))
                                    found_complete_matches.add(signature)

            # 计算各种未找到的函数
            not_found_in_source = functions_to_find - found_in_source
            not_found_in_output = functions_to_find - found_in_output

            # 打印调试信息
            print(f"\n[Replacement DEBUG] Functions not found in source ({len(not_found_in_source)}) => {not_found_in_source}")
            print(f"[Replacement DEBUG] Functions not found in output ({len(not_found_in_output)}) => {not_found_in_output}")
            print(f"[Replacement DEBUG] Successfully matched and replaced => {found_complete_matches}")
            
            print(f"\nTotal replacements to make: {len(replacements)}")

            # 在 output_code 中替换相应函数体
            for start, end, new_content in sorted(replacements, reverse=True):
                modified_code = modified_code[:start] + new_content + modified_code[end:]

            # 返回替换后的代码 以及 本次处理需要的缺失信息
            return modified_code, not_found_in_source, not_found_in_output

        except Exception as e:
            print(f"[ERROR] Error processing file {source_file}: {str(e)}")
            # 出错时，无法完成替换，返回 None
            return None, set(), set()

    def process_test_dependencies(self, source_path, output_path, dependencies, json_log_path="~/missing_dependencies.json"):
        """
        Process test dependencies
        Args:
            source_path: Path to source code (containing the original implementations)
            output_path: Path for output (containing the files to be modified)
            dependencies: List of dependency information
            json_log_path: File path for output JSON log of missing dependencies
        """
        # 用于记录所有未找到的依赖（包括文件不存在、函数在源文件或输出文件里未找到）
        missing_dependencies_log = []

        # 按文件进行分组
        file_dependencies = {}
        for dep in dependencies:
            file_dependencies.setdefault(dep['file'], []).append(dep)

        # 处理每个文件
        for file_path, deps in file_dependencies.items():
            source_file = os.path.join(source_path, file_path)
            output_file = os.path.join(output_path, file_path)

            # 如果源文件不存在，则该文件下的所有依赖都标记为 file_not_found
            if not os.path.exists(source_file):
                print(f"[WARNING] Source file does not exist: {file_path}")
                for dep in deps:
                    missing_dependencies_log.append({
                        "file": file_path,
                        "function": dep['source_function'],
                        "parameter_types": dep['parameter_types'],
                        "reason": "file_not_found"
                    })
                continue  # 跳过后续替换

            print(f"[DEBUG] Processing file: {file_path}")
            
            # 替换并获取没有找到的函数信息
            modified_code, not_found_in_source, not_found_in_output = self.replace_functions_in_file(
                source_file, output_file, deps
            )
            
            # 如果替换出错，则跳过写入
            if modified_code is None:
                continue

            # 记录“函数未在源文件找到”
            for func_name, param_types in not_found_in_source:
                missing_dependencies_log.append({
                    "file": file_path,
                    "function": func_name,
                    "parameter_types": param_types,
                    "reason": "function_not_found_in_source"
                })

            # 记录“函数未在输出文件找到”（即没有可以替换的位置）
            for func_name, param_types in not_found_in_output:
                missing_dependencies_log.append({
                    "file": file_path,
                    "function": func_name,
                    "parameter_types": param_types,
                    "reason": "function_not_found_in_output"
                })

            # 如果成功获取了替换后的内容，则写回 output_file
            print(f"[DEBUG] Writing modified file: {output_file}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(modified_code)

        # 最后，将所有未找到的依赖信息写入 JSON 文件
        if missing_dependencies_log:
            print(f"[INFO] Writing missing dependencies log to: {json_log_path}")
            with open(json_log_path, 'w', encoding='utf-8') as jf:
                json.dump({"missing_dependencies": missing_dependencies_log}, jf, indent=4)
        else:
            print("[INFO] All dependencies found. No missing dependencies to log.")
