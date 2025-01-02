import os
import shutil
import argparse
import warnings
from tree_sitter_languages import get_language, get_parser

warnings.filterwarnings("ignore", category=FutureWarning)

language = get_language("java")
parser = get_parser("java")

def get_default_return_statement(return_type):
    return_type = return_type.strip()
    if return_type in ['int', 'long', 'short', 'byte']:
        return 'return 0;'
    elif return_type == 'boolean':
        return 'return false;'
    elif return_type == 'double':
        return 'return 0.0;'
    elif return_type == 'float':
        return 'return 0.0f;'
    elif return_type == 'char':
        return "return 'a';"
    elif return_type == 'String':
        return 'return "";'
    elif return_type == 'void':
        return 'return;'
    elif return_type.endswith('[]'):
        return f'return new {return_type[:-2]}[0];'
    else:
        return 'return null;'  # deal with object and self-defined class

# iteratively search method_declaration、constructor_declaration 和 static_initializer nodes
def find_relevant_nodes(node):
    relevant_nodes = []
    if node.type in ['method_declaration', 'constructor_declaration', 'static_initializer']:
        relevant_nodes.append(node)
    for child in node.children:
        relevant_nodes.extend(find_relevant_nodes(child))
    return relevant_nodes   

# search and return 'assignment_expression' nodes
def get_assignment_expression(statement_node):
    for child in statement_node.children:
        if child.type == 'assignment_expression':
            return child
    return None

def is_assignment_statement(statement_node, source_code):
    if statement_node.type == 'expression_statement':
        expr = get_assignment_expression(statement_node)
        if expr and expr.type == 'assignment_expression':
            print(f"Identified assignment_expression: {source_code[expr.start_byte:expr.end_byte].decode('utf-8', errors='replace').strip()}")
            return True
    elif statement_node.type == 'local_declaration_statement':
        declaration = statement_node.child_by_field_name('declaration')
        if declaration and declaration.type == 'variable_declaration':
            for declarator in declaration.children:
                if declarator.type == 'variable_declarator':
                    initializer = declarator.child_by_field_name('initializer')
                    if initializer:
                        print(f"Identified variable initializer: {source_code[initializer.start_byte:initializer.end_byte].decode('utf-8', errors='replace').strip()}")
                        return True
    return False

def get_indentation(source_code_bytes, start_byte):
    line_start = source_code_bytes.rfind(b'\n', 0, start_byte) + 1
    indentation = b''
    while line_start < start_byte:
        b_char = source_code_bytes[line_start]
        if b_char == ord(' ') or b_char == ord('\t'):
            indentation += bytes([b_char])
            line_start += 1
        else:
            break
    return indentation.decode('utf-8')

def debug_print_node(node, source_code, depth=0):
    indent = '  ' * depth
    node_text = source_code[node.start_byte:node.end_byte].decode('utf-8', errors='replace').strip()
    print(f"{indent}{node.type} [{node.start_point} - {node.end_point}]: {node_text[:30]}...")
    for child in node.children:
        debug_print_node(child, source_code, depth + 1)

# modify function and static blocks
def modify_function_and_static_blocks(tree, source_code_bytes):
    root_node = tree.root_node

    debug_print_node(root_node, source_code_bytes)
    print("\n-----------------------------------\n")

    relevant_nodes = find_relevant_nodes(root_node)

    replacements = []
    for node in relevant_nodes:
        if node.type in ['method_declaration', 'constructor_declaration']:
            if node.type == 'method_declaration':
                return_type_node = node.child_by_field_name('type')
                if not return_type_node:
                    continue
                return_type_bytes = source_code_bytes[return_type_node.start_byte:return_type_node.end_byte]
                return_type = return_type_bytes.decode('utf-8').strip()
                return_statement = get_default_return_statement(return_type)
            else:
                return_statement = ""

            body_node = node.child_by_field_name('body')
            if body_node:
                start_byte = body_node.start_byte + 1
                end_byte = body_node.end_byte - 1

                indentation_str = get_indentation(source_code_bytes, body_node.start_byte)

                if return_statement:
                    new_body = f'\n{indentation_str}    {return_statement}\n{indentation_str}'
                else:
                    new_body = f'\n{indentation_str}\n{indentation_str}'

                replacements.append((start_byte, end_byte, new_body.encode('utf-8')))

        elif node.type == 'static_initializer':
            print(f"Processing static_initializer node: [{node.start_point} - {node.end_point}]")
            debug_print_node(node, source_code_bytes, depth=1)

            block_node = node.child_by_field_name('block')
            if not block_node:
                for child in node.children:
                    if child.type == 'block':
                        block_node = child
                        break

            if block_node:
                assignment_statements = []
                for statement in block_node.children:
                    if is_assignment_statement(statement, source_code_bytes):
                        statement_text = source_code_bytes[statement.start_byte:statement.end_byte].decode('utf-8', errors='replace').strip()
                        assignment_statements.append(statement_text)

                indentation_str = get_indentation(source_code_bytes, block_node.start_byte)

                if assignment_statements:
                    assignments_joined = '\n'.join([f"{indentation_str}    {stmt}" for stmt in assignment_statements])

                    new_body = f'\n{assignments_joined}\n{indentation_str}'
                else:
                    new_body = f'\n{indentation_str}\n{indentation_str}'

                start_byte = block_node.start_byte + 1
                end_byte = block_node.end_byte - 1

                replacements.append((start_byte, end_byte, new_body.encode('utf-8')))
            else:
                print("warning: static_initializer's block node not found\n")

    replacements.sort(reverse=True, key=lambda x: x[0])

    # apply the replacement
    modified_code = bytearray(source_code_bytes)
    for start, end, new_body in replacements:
        modified_code[start:end] = new_body

    return modified_code.decode('utf-8')

# process single java file
def process_java_file(file_path, input_dir, output_dir):
    with open(file_path, 'rb') as f:
        source_code_bytes = f.read()

    tree = parser.parse(source_code_bytes)
    modified_code = modify_function_and_static_blocks(tree, source_code_bytes)

    relative_path = os.path.relpath(file_path, start=input_dir)
    output_file_path = os.path.join(output_dir, relative_path)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(modified_code)
    print(f"Processed Java file: {relative_path}\n")

def copy_non_java_file(file_path, input_dir, output_dir):
    relative_path = os.path.relpath(file_path, start=input_dir)
    output_file_path = os.path.join(output_dir, relative_path)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    shutil.copy2(file_path, output_file_path)
    print(f"Copied non-Java file: {relative_path}\n")

def process_java_directory(input_dir, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}\n")

    for root, dirs, files in os.walk(input_dir):
        relative_root = os.path.relpath(root, input_dir)
        destination_root = os.path.join(output_dir, relative_root)
        os.makedirs(destination_root, exist_ok=True)
        if relative_root != '.':
            print(f"Created directory: {relative_root}")

        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".java"):
                process_java_file(file_path, input_dir, output_dir)
            else:
                copy_non_java_file(file_path, input_dir, output_dir)

def main():
    arg_parser = argparse.ArgumentParser(description='Process Java files by replacing function bodies with simple return statements, and copy other files to the output directory.')
    arg_parser.add_argument('input_dir', type=str, help='Path to the input Java project directory')
    arg_parser.add_argument('output_dir', type=str, help='Path to the output directory for modified Java files and other files')

    args = arg_parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    print(f"Starting processing...\nInput Directory: {input_dir}\nOutput Directory: {output_dir}\n")

    process_java_directory(input_dir, output_dir)
    print("\nProcessing completed successfully.")

if __name__ == "__main__":
    main()
