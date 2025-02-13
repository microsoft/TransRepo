from typing import Optional
from tree_sitter import Node

class JavaFileProcessor:
    @staticmethod
    def debug_print_node(node: Node, source_code: bytes, depth: int = 0) -> None:
        """print node information"""
        indent = '  ' * depth
        node_text = source_code[node.start_byte:node.end_byte].decode('utf-8', errors='replace').strip()
        print(f"{indent}{node.type} [{node.start_point} - {node.end_point}]: {node_text[:30]}...")
        for child in node.children:
            JavaFileProcessor.debug_print_node(child, source_code, depth + 1)