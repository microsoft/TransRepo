import tree_sitter
from tree_sitter import Language, Parser
import os
import shutil

class FunctionReplacer:
    def __init__(self, grammar_path='/home/v-jiahengwen/RepoTranslationAgent/src/dependency/build/my-languages.so'):
        """
        Initialize FunctionReplacer
        Args:
            grammar_path: Path to the tree-sitter grammar library
        """
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
            
            source_tree = self.java_parser.parse(bytes(source_code, 'utf8'))
            output_tree = self.java_parser.parse(bytes(output_code, 'utf8'))

            # 修改查询以同时包含方法声明和构造函数
            query = self.JAVA_LANGUAGE.query("""
                (method_declaration
                    name: (identifier) @method_name) @method
                (constructor_declaration
                    name: (identifier) @constructor_name) @constructor
            """)
            
            source_methods = {}
            # print("[Replacement DEBUG] Scanning source file for methods and constructors...")
            
            for node, capture_name in query.captures(source_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)
                    signature = (method_name, param_types)
                    
                    # if node.type == 'constructor_declaration':
                        # print(f"[Replacement DEBUG] Found constructor in source: {method_name} with params {param_types}")
                    
                    # 检查是否是我们要找的函数
                    if signature in functions_to_find:
                        found_in_source.add(signature)
                    
                    # 记录函数名匹配的情况
                    if method_name in function_names_to_find:
                        if method_name not in name_only_matches_in_source:
                            name_only_matches_in_source[method_name] = []
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
                        if method_name not in name_only_matches_in_output:
                            name_only_matches_in_output[method_name] = []
                        name_only_matches_in_output[method_name].append((param_types, signature))
                        
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

    def process_test_dependencies(self, source_path, output_path, dependencies):
        """
        Process test dependencies
        Args:
            source_path: Path to source code (containing the original implementations)
            output_path: Path for output (containing the files to be modified)
            dependencies: List of dependency information
        """
        # Group dependencies by file
        file_dependencies = {}
        for dep in dependencies:
            file_dependencies.setdefault(dep['file'], []).append(dep)

        # Process each file
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