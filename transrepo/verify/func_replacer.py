import tree_sitter
from tree_sitter import Language, Parser
import os
import shutil

class FunctionReplacer:
    def __init__(self, grammar_path='../baseline/build/my-languages.so'):
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
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            with open(output_file, 'r', encoding='utf-8') as f:
                output_code = f.read()
            
            source_tree = self.java_parser.parse(bytes(source_code, 'utf8'))
            output_tree = self.java_parser.parse(bytes(output_code, 'utf8'))

            # Create a map of function signatures to their implementation in source file
            source_methods = {}
            query = self.JAVA_LANGUAGE.query("""
                (method_declaration
                name: (identifier) @method_name) @method
            """)
            
            for method_node, _ in query.captures(source_tree.root_node):
                if method_node.type == 'method_declaration':
                    method_name = method_node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(method_node)
                    
                    # Find the end position of the method body
                    body = method_node.child_by_field_name('body')
                    if body:
                        # Ensure including the last "}"
                        end_byte = body.end_byte
                        # Check characters after method body in source code to ensure complete brackets
                        while end_byte < len(source_code.encode('utf8')) and source_code.encode('utf8')[end_byte-1:end_byte] != b'}':
                            end_byte += 1
                        
                        source_methods[(method_name, param_types)] = (
                            method_node.start_byte,
                            end_byte,
                            source_code[method_node.start_byte:end_byte]
                        )

            # Find and replace matching methods in output file
            modified_code = output_code
            replacements = []  # Store (start, end, new_content) tuples
            
            query = self.JAVA_LANGUAGE.query("""
                (method_declaration
                name: (identifier) @method_name) @method
            """)
            
            for method_node, _ in query.captures(output_tree.root_node):
                if method_node.type == 'method_declaration':
                    method_name = method_node.child_by_field_name('name').text.decode('utf8')
                    param_types = self.get_parameter_types(method_node)
                    
                    # Check if this method should be replaced
                    for dep in dependencies:
                        if (dep['source_function'] == method_name and 
                            dep['parameter_types'] == param_types):
                            print(f"[Replacer] debugging, {method_name} found successfully")
                            # Find corresponding implementation in source file
                            source_method = source_methods.get((method_name, param_types))
                            if source_method:
                                # Similarly ensure complete end position for target method
                                body = method_node.child_by_field_name('body')
                                if body:
                                    end_byte = body.end_byte
                                    while end_byte < len(output_code.encode('utf8')) and output_code.encode('utf8')[end_byte-1:end_byte] != b'}':
                                        end_byte += 1
                                    
                                    replacements.append((
                                        method_node.start_byte,
                                        end_byte,
                                        source_method[2]
                                    ))
                            break

            # Apply replacements in reverse order to maintain byte positions
            for start, end, new_content in sorted(replacements, reverse=True):
                modified_code = modified_code[:start] + new_content + modified_code[end:]

            return modified_code

        except Exception as e:
            print(f"[WARNING] Error processing file {source_file}: {str(e)}")
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

            if not os.path.exists(source_file) or not os.path.exists(output_file):
                print(f"[WARNING] Source or output file does not exist: {file_path}")
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