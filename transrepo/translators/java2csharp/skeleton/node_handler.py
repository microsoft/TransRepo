from typing import List, Tuple, Optional
from tree_sitter import Node, Tree
from core.utils.file_utils import FileUtils

class JavaNodeHandler:
    @staticmethod
    def get_default_return_statement(return_type: str) -> str:
        """Get default return statement based on the return type."""
        return_type = return_type.strip()
        type_map = {
            'int': 'return 0;',
            'long': 'return 0;',
            'short': 'return 0;',
            'byte': 'return 0;',
            'boolean': 'return false;',
            'double': 'return 0.0;',
            'float': 'return 0.0f;',
            'char': "return 'a';",
            'String': 'return "";',
            'void': 'return;'
        }
        
        if return_type in type_map:
            return type_map[return_type]
        elif return_type.endswith('[]'):
            return f'return new {return_type[:-2]}[0];'
        return 'return null;'

    def find_relevant_nodes(self, node: Node) -> List[Node]:
        """Recursively find relevant nodes (methods, constructors, static initializers)."""
        relevant_nodes = []
        if node.type in ['method_declaration', 'constructor_declaration', 'static_initializer']:
            relevant_nodes.append(node)
        for child in node.children:
            relevant_nodes.extend(self.find_relevant_nodes(child))
        return relevant_nodes

    def is_assignment_statement(self, statement_node: Node, source_code: bytes) -> bool:
        """Determine if a statement is an assignment statement."""
        if statement_node.type == 'expression_statement':
            expr = self.get_assignment_expression(statement_node)
            if expr and expr.type == 'assignment_expression':
                return True
        elif statement_node.type == 'local_declaration_statement':
            declaration = statement_node.child_by_field_name('declaration')
            if declaration and declaration.type == 'variable_declaration':
                for declarator in declaration.children:
                    if declarator.type == 'variable_declarator':
                        initializer = declarator.child_by_field_name('initializer')
                        if initializer:
                            return True
        return False

    @staticmethod
    def get_assignment_expression(statement_node: Node) -> Optional[Node]:
        """Get the assignment expression in a statement, if it exists."""
        for child in statement_node.children:
            if child.type == 'assignment_expression':
                return child
        return None

    def modify_function_and_static_blocks(self, tree: Tree, source_code_bytes: bytes) -> str:
        """Modify the function bodies and static blocks in the source code."""
        root_node = tree.root_node
        relevant_nodes = self.find_relevant_nodes(root_node)
        replacements = []

        for node in relevant_nodes:
            if node.type in ['method_declaration', 'constructor_declaration']:
                self._handle_method_or_constructor(node, source_code_bytes, replacements)
            elif node.type == 'static_initializer':
                self._handle_static_initializer(node, source_code_bytes, replacements)

        # Sort replacements in reverse order to avoid index shifting issues
        replacements.sort(reverse=True, key=lambda x: x[0])
        modified_code = bytearray(source_code_bytes)
        
        # Apply replacements
        for start, end, new_body in replacements:
            modified_code[start:end] = new_body

        return modified_code.decode('utf-8')

    def _handle_method_or_constructor(self, node: Node, source_code_bytes: bytes, replacements: List[Tuple[int, int, bytes]]) -> None:
        """Handle method or constructor node modification."""
        if node.type == 'method_declaration':
            return_type_node = node.child_by_field_name('type')
            if not return_type_node:
                return
            return_type = source_code_bytes[return_type_node.start_byte:return_type_node.end_byte].decode('utf-8').strip()
            return_statement = self.get_default_return_statement(return_type)
        else:
            return_statement = ""

        body_node = node.child_by_field_name('body')
        if body_node:
            indentation = self._get_indentation(source_code_bytes, body_node.start_byte)
            new_body = (
                f'\n{indentation}    {return_statement}\n{indentation}' 
                if return_statement 
                else f'\n{indentation}\n{indentation}'
            )
            replacements.append((body_node.start_byte + 1, body_node.end_byte - 1, new_body.encode('utf-8')))

    def _handle_static_initializer(self, node: Node, source_code_bytes: bytes, replacements: List[Tuple[int, int, bytes]]) -> None:
        """Handle static initializer block modification."""
        block_node = node.child_by_field_name('block') or next((child for child in node.children if child.type == 'block'), None)
        if not block_node:
            return

        assignment_statements = []
        for statement in block_node.children:
            if self.is_assignment_statement(statement, source_code_bytes):
                stmt_text = source_code_bytes[statement.start_byte:statement.end_byte].decode('utf-8', errors='replace').strip()
                assignment_statements.append(stmt_text)

        indentation = self._get_indentation(source_code_bytes, block_node.start_byte)
        if assignment_statements:
            assignments_joined = '\n'.join([f"{indentation}    {stmt}" for stmt in assignment_statements])
            new_body = f'\n{assignments_joined}\n{indentation}'
        else:
            new_body = f'\n{indentation}\n{indentation}'

        replacements.append((block_node.start_byte + 1, block_node.end_byte - 1, new_body.encode('utf-8')))

    @staticmethod
    def _get_indentation(source_code_bytes: bytes, start_byte: int) -> str:
        """Helper to get indentation before a given byte offset."""
        line_start = source_code_bytes.rfind(b'\n', 0, start_byte) + 1
        indentation = b''
        while line_start < start_byte:
            b_char = source_code_bytes[line_start]
            if b_char in (ord(' '), ord('\t')):
                indentation += bytes([b_char])
                line_start += 1
            else:
                break
        return indentation.decode('utf-8')