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
        Extract parameter types from a method or constructor node
        """
        parameters = []
        formal_parameters = method_node.child_by_field_name('parameters')  # Updated field name
        
        if not formal_parameters:
            print(f"[DEBUG] No 'parameters' field found in node type: {method_node.type}")
        
        if formal_parameters:
            for param in formal_parameters.children:
                # print(f"[DEBUG] Processing parameter node: {param.type}")
                if param.type == 'parameter':
                    type_node = param.child_by_field_name('type')
                    if type_node:
                        param_type = type_node.text.decode('utf8')
                        # print(f"[DEBUG] Found parameter type: {param_type}")
                        parameters.append(param_type)
                    else:
                        print("[DEBUG] No 'type' field found for parameter")
        
        return ','.join(parameters) if parameters else 'None'

    def replace_functions_in_file(self, source_file, output_file, dependencies):
        """
        Replace multiple functions in a file based on function name and parameter types,
        but only replace the inside of the method body, leaving original signature and outer braces intact.
        This version is more robust in searching the actual '{' and '}' in the target file
        to avoid missing braces due to whitespace or new lines.
        """
        print(f"[Replacement DEBUG] Total functions to replace: {len(dependencies)}")
        # print("[Replacement DEBUG] Functions to find:", 
        #     [(d['source_function'], d['parameter_types']) for d in dependencies])
        
        functions_to_find = set((d['source_function'], d['parameter_types']) for d in dependencies)
        function_names_to_find = set(d['source_function'] for d in dependencies)

        found_in_source = set()
        found_in_output = set()
        found_complete_matches = set()
        name_only_matches_in_source = {}
        name_only_matches_in_output = {}

        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            with open(output_file, 'r', encoding='utf-8') as f:
                output_code = f.read()
            
            source_tree = self.csharp_parser.parse(bytes(source_code, 'utf8'))
            output_tree = self.csharp_parser.parse(bytes(output_code, 'utf8'))

            # 修改查询以同时包含方法声明和构造函数
            query = self.JAVA_LANGUAGE.query("""
                (method_declaration
                    name: (identifier) @method_name) @method
                (constructor_declaration
                    name: (identifier) @constructor_name
                    parameters: (parameter_list)?
                    initializer: (constructor_initializer
                                    (argument_list)? )? ) @constructor
            """)
            
            source_methods = {}
            # print("[Replacement DEBUG] Scanning source file for methods and constructors...")
            
            for node, capture_name in query.captures(source_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)  # User-defined function
                    signature = (method_name, param_types)
                    
                    # if node.type == 'constructor_declaration':
                        # print(f"[Replacement DEBUG] Found constructor in source: {method_name} with params {param_types}")
                    
                    # 检查是否是我们要找的函数
                    if signature in functions_to_find:
                        found_in_source.add(signature)
                    
                    # 记录函数名匹配的情况
                    if method_name in function_names_to_find:
                        name_only_matches_in_source.setdefault(method_name, [])
                        name_only_matches_in_source[method_name].append((param_types, signature))
                    
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
            
            # print(f"[Replacement DEBUG] Found {len(source_methods)} total methods/constructors in source file")
            # print("[Replacement DEBUG] Methods/constructors found in source that we're looking for:", found_in_source)

            # Find and replace matching methods in output file
            modified_code = output_code
            replacements = []

            for node, capture_name in query.captures(output_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)
                    signature = (method_name, param_types)
                    
                    if node.type == 'constructor_declaration':
                        print(f"[Replacement DEBUG] Found constructor in output: {method_name} with params {param_types}")
                    
                    if signature in functions_to_find:
                        found_in_output.add(signature)
                    
                    # 记录函数名匹配的情况
                    if method_name in function_names_to_find:
                        name_only_matches_in_output.setdefault(method_name, [])
                        name_only_matches_in_output[method_name].append((param_types, signature))
                        
                        if signature in found_in_source:
                            source_body_inside = source_methods.get(signature, None)
                            if source_body_inside is None:
                                continue

                            body_node = node.child_by_field_name('body')
                            if body_node is not None:
                                b_start = body_node.start_byte
                                b_end   = body_node.end_byte

                            if b_end > b_start + 2:
                                # Find actual '{' and '}' in this region to avoid offset due to whitespace or newlines
                                original_body_text = output_code[b_start : b_end]
                                print(f"See this sucking original body text of {method_name}:\n{original_body_text}")
                                # Find '{' from left to right
                                left_brace_index = 0
                                while left_brace_index < len(original_body_text) and original_body_text[left_brace_index] not in ['{']:
                                    left_brace_index += 1

                                # Find '}' from right to left
                                right_brace_index = len(original_body_text) - 1
                                while right_brace_index > 0 and original_body_text[right_brace_index] not in ['}']:
                                    right_brace_index -= 1

                                if(left_brace_index > right_brace_index):
                                    output_code = '{' + output_code
                                    left_brace_index = 0

                                # If positions are found, construct replacement interval
                                # out_inside_start/out_inside_end used for only-body replacement
                                # b_start + left_brace_index is position of '{'
                                out_inside_start = b_start + left_brace_index + 1
                                out_inside_end   = b_start + right_brace_index

                                # If left_brace_index or right_brace_index is invalid, skip
                                if (out_inside_start <= out_inside_end and
                                        0 <= left_brace_index < right_brace_index < len(original_body_text)):
                                    replacements.append((out_inside_start, out_inside_end, source_body_inside))
                                    found_complete_matches.add(signature)

            # 计算各种情况的函数
            not_found_in_source = functions_to_find - found_in_source
            not_found_in_output = functions_to_find - found_in_output
            found_but_no_match = (found_in_source & found_in_output) - found_complete_matches

            # print("\n[Replacement DEBUG] Function Finding Status:")
            # print(f"Functions not found in source file ({len(not_found_in_source)}):", not_found_in_source)
            # print(f"Functions not found in output file ({len(not_found_in_output)}):", not_found_in_output)
            # print(f"Functions found in both files but couldn't be matched ({len(found_but_no_match)}):", found_but_no_match)
            # print(f"Successfully matched functions ({len(found_complete_matches)}):", found_complete_matches)
            
            # print("\n[Replacement DEBUG] Name-only matches:")
            # for func_name in function_names_to_find:
            #     print(f"\nFunction name: {func_name}")
            #     print("In source file:", 
            #         name_only_matches_in_source.get(func_name, []))
            #     print("In output file:", 
            #         name_only_matches_in_output.get(func_name, []))
                
            print(f"\nTotal replacements to make: {len(replacements)}")

            # Apply replacements in reverse order to maintain byte positions
            for start, end, new_content in sorted(replacements, reverse=True):
                # print("[Replacement DEBUG] Applying replacement...")
                modified_code = modified_code[:start] + new_content + modified_code[end:]

            return modified_code

        except Exception as e:
            print(f"[ERROR] Error processing file {source_file}: {str(e)}")
            return None

    def process_test_dependencies(self, source_path, output_path, dependencies, json_log_path="~/missing_dependencies.json"):
        """
        Process test dependencies
        Args:
            source_path: Path to source code (containing the original implementations)
            output_path: Path for output (containing the files to be modified)
            dependencies: List of dependency information
            json_log_path: File path for output JSON log of missing dependencies
        """
        # Group dependencies by file
        file_dependencies = {}
        for dep in dependencies:
            file_dependencies.setdefault(dep['file'], []).append(dep)

        # 处理每个文件
        for file_path, deps in file_dependencies.items():
            source_file = os.path.join(source_path, file_path)
            output_file = os.path.join(output_path, file_path)

            # if not os.path.exists(source_file) or not os.path.exists(output_file):
            if not os.path.exists(source_file):
                print(f"[WARNING] Source file does not exist: {file_path}")
                print(f"[WARNING] Source file path:{source_file}")
                continue

            print(f"[DEBUG] Processing file: {file_path}")
            
            # Replace all matching functions in the file
            print(f"[DEBUG]:")
            modified_code = self.replace_functions_in_file(source_file, output_file, deps)
            
            if modified_code:
                print(f"[DEBUG] Writing modified file: {output_file}")
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(modified_code)