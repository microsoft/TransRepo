import json
import os
import shutil
import tree_sitter
from tree_sitter import Language, Parser

class FunctionReplacer:
    def __init__(self, grammar_path='/home/v-jiahengwen/RepoTranslationAgent/src/dependency/build/my-languages.so'):
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

        # Method signatures to replace (method_name, [param_type, param_type, ...])
        functions_to_find = set((d['source_function'], d['parameter_types']) for d in dependencies)
        function_names_to_find = set(d['source_function'] for d in dependencies)

        found_in_source = set()
        found_in_output = set()
        found_complete_matches = set()

        # Statistics for name-only matches with mismatched parameters
        name_only_matches_in_source = {}
        name_only_matches_in_output = {}

        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            with open(output_file, 'r', encoding='utf-8') as f:
                output_code = f.read()
            
            source_tree = self.csharp_parser.parse(bytes(source_code, 'utf8'))
            output_tree = self.csharp_parser.parse(bytes(output_code, 'utf8'))

            # Match both method declarations and constructors
            query = self.CSHARP_LANGUAGE.query(r"""
                (method_declaration
                    name: (identifier) @method_name
                    parameters: (parameter_list)? ) @method

                (constructor_declaration
                    name: (identifier) @constructor_name
                    parameters: (parameter_list)?
                    initializer: (constructor_initializer
                                    (argument_list)? )? ) @constructor
            """)

            # ---------------------------------------------------------------------
            # 1) Extract the "text inside braces" from each target method or constructor body in source file
            # ---------------------------------------------------------------------
            source_methods = {}
            for node, capture_name in query.captures(source_tree.root_node):
                if node.type in ['method_declaration', 'constructor_declaration']:
                    method_name = node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(node)  # User-defined function
                    signature = (method_name, param_types)

                    # If this is a function to be replaced
                    if signature in functions_to_find:
                        found_in_source.add(signature)

                    if method_name in function_names_to_find:
                        name_only_matches_in_source.setdefault(method_name, [])
                        name_only_matches_in_source[method_name].append((param_types, signature))

                    body_node = node.child_by_field_name('body')
                    if body_node is not None:
                        body_start = body_node.start_byte
                        body_end = body_node.end_byte

                        # Basic check: must have {}
                        if body_end > body_start + 2:
                            # tree-sitter usually ensures body_start points to '{' and body_end-1 points to '}' or following whitespace
                            # First take the middle region
                            # Get original body from source file
                            original_body_text = source_code[body_start : body_end]

                            # Find '{' from left to right
                            left_brace_index = 0
                            while left_brace_index < len(original_body_text) and original_body_text[left_brace_index] not in ['{']:
                                left_brace_index += 1

                            # Find '}' from right to left
                            right_brace_index = len(original_body_text) - 1
                            while right_brace_index > 0 and original_body_text[right_brace_index] not in ['}']:
                                right_brace_index -= 1

                            # Inside is everything between { and }
                            inside_start = left_brace_index + 1
                            inside_end   = right_brace_index

                            if inside_end < inside_start:
                                # If braces not found, skip
                                source_methods[signature] = ""
                            else:
                                body_inside = original_body_text[inside_start:inside_end]
                                source_methods[signature] = body_inside
                        else:
                            # Empty function body
                            source_methods[signature] = ""

            # ---------------------------------------------------------------------
            # 2) Traverse target file, search for matching methods or constructors, and "only replace inside braces";
            #    preserve external signature and braces
            # ---------------------------------------------------------------------
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
                                else:
                                # Avoid exceptional cases
                                    if(not out_inside_start <= out_inside_end):
                                        print("-------Fucking Rat is here-------")
                                        print(f"out_inside_start: {out_inside_start}")
                                        print(f"out_inside_end: {out_inside_end}")
                                        print(f"left_brace_index: {left_brace_index}")
                                        print(f"right_brace_index: {right_brace_index}")
                                    else:
                                        print(f"left_brace_index is {left_brace_index}\nright_brace_index is {right_brace_index}\nlen(original_body_text) is {len(original_body_text)} ")
                                    pass

            # ---------------------------------------------------------------------
            # 3) Count functions not found
            # ---------------------------------------------------------------------
            not_found_in_source = functions_to_find - found_in_source
            not_found_in_output = functions_to_find - found_in_output

            print(f"[Replacement DEBUG] Functions not found in source ({len(not_found_in_source)}) => {not_found_in_source}")
            print(f"[Replacement DEBUG] Functions not found in output ({len(not_found_in_output)}) => {not_found_in_output}")
            print(f"[Replacement DEBUG] Successfully matched and replaced => {found_complete_matches}")

            print(f"[Replacement DEBUG] Total replacements to make: {len(replacements)}")

            # ---------------------------------------------------------------------
            # 4) Execute replacements (in reverse order to avoid index offset issues)
            # ---------------------------------------------------------------------
            for start_idx, end_idx, new_content in sorted(replacements, reverse=True):
                modified_code = (
                    modified_code[:start_idx] 
                    + new_content 
                    + modified_code[end_idx:]
                )

            return modified_code, not_found_in_source, not_found_in_output

        except Exception as e:
            print(f"[ERROR] Error processing file {source_file}: {str(e)}")
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
        # Track all missing dependencies (including non-existent files, functions not found in source or output)
        missing_dependencies_log = []

        # Group by file
        file_dependencies = {}
        for dep in dependencies:
            file_dependencies.setdefault(dep['file'], []).append(dep)

        # Process each file
        for file_path, deps in file_dependencies.items():
            source_file = os.path.join(source_path, file_path)
            output_file = os.path.join(output_path, file_path)

            # If source file doesn't exist, mark all dependencies as file_not_found
            if not os.path.exists(source_file):
                print(f"[WARNING] Source file does not exist: {file_path}")
                for dep in deps:
                    missing_dependencies_log.append({
                        "file": file_path,
                        "function": dep['source_function'],
                        "parameter_types": dep['parameter_types'],
                        "reason": "file_not_found"
                    })
                continue  # Skip replacement

            print(f"[DEBUG] Processing file: {file_path}")
            
            # Replace and get information about functions not found
            modified_code, not_found_in_source, not_found_in_output = self.replace_functions_in_file(
                source_file, output_file, deps
            )
            
            # Skip writing if replacement failed
            if modified_code is None:
                continue

            # Record "function not found in source file"
            for func_name, param_types in not_found_in_source:
                missing_dependencies_log.append({
                    "file": file_path,
                    "function": func_name,
                    "parameter_types": param_types,
                    "reason": "function_not_found_in_source"
                })

            # Record "function not found in output file" (no replacement location)
            for func_name, param_types in not_found_in_output:
                missing_dependencies_log.append({
                    "file": file_path,
                    "function": func_name,
                    "parameter_types": param_types,
                    "reason": "function_not_found_in_output"
                })

            # If replacement content was successfully obtained, write back to output_file
            print(f"[DEBUG] Writing modified file: {output_file}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(modified_code)

        # Finally, write all missing dependency information to JSON file
        if missing_dependencies_log:
            print(f"[INFO] Writing missing dependencies log to: {json_log_path}")
            with open(json_log_path, 'a', encoding='utf-8') as jf:
                json.dump({"missing_dependencies": missing_dependencies_log}, jf, indent=4)
        else:
            print("[INFO] All dependencies found. No missing dependencies to log.")