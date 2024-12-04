import os
import shutil
import warnings
from tree_sitter_languages import get_language, get_parser

class NamespaceFixer:
    def __init__(self):
        # Suppress FutureWarning to hide deprecation messages
        warnings.filterwarnings("ignore", category=FutureWarning)
        
        # Initialize C# language and parser using tree-sitter
        self.language = get_language("c_sharp")
        self.parser = get_parser("c_sharp")
        
        # Initialize tracking lists
        self.successful_usings = []
        self.fixed_usings = []
        self.failed_usings = []

    def collect_namespaces_and_types(self, input_dir):
        defined_namespaces = set()
        defined_types = set()
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        source_code = f.read()
                    tree = self.parser.parse(source_code)
                    root_node = tree.root_node
                    namespaces, types = self._extract_namespaces_and_types(root_node, source_code)
                    defined_namespaces.update(namespaces)
                    defined_types.update(types)
        return defined_namespaces, defined_types

    def _extract_namespaces_and_types(self, node, source_code, current_namespace=None):
        namespaces = set()
        types = set()
        
        if node.type == 'namespace_declaration':
            name_node = node.child_by_field_name('name')
            if name_node:
                namespace = self._get_node_text(name_node, source_code)
                namespaces.add(namespace)
                current_namespace = namespace
        elif node.type in ['class_declaration', 'struct_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration']:
            name_node = node.child_by_field_name('name')
            if name_node and current_namespace:
                type_name = self._get_node_text(name_node, source_code)
                full_type_name = f"{current_namespace}.{type_name}"
                types.add(full_type_name)
            elif node.type in ['class_declaration', 'struct_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    type_name = self._get_node_text(name_node, source_code)
                    types.add(type_name)
        
        for child in node.children:
            child_namespaces, child_types = self._extract_namespaces_and_types(child, source_code, current_namespace)
            namespaces.update(child_namespaces)
            types.update(child_types)
        
        return namespaces, types

    def _get_node_text(self, node, source_code):
        return source_code[node.start_byte:node.end_byte].decode('utf-8', errors='replace').strip()

    def _process_csharp_file(self, file_path, input_dir, output_dir, defined_namespaces, defined_types):
        with open(file_path, 'rb') as f:
            source_code_bytes = f.read()
        
        tree = self.parser.parse(source_code_bytes)
        root_node = tree.root_node

        usings = [node for node in root_node.children if node.type == 'using_directive']
        replacements = []
        
        for using_node in usings:
            name_node = using_node.child_by_field_name('name')
            if not name_node:
                continue
            using_namespace = self._get_node_text(name_node, source_code_bytes)
            
            # 处理系统命名空间
            if using_namespace.startswith(("System", "NUnit")):
                self.successful_usings.append(using_namespace)
                continue

            fixed = False
            # 检查和修复命名空间
            for defined_ns in defined_namespaces.union(defined_types):
                if self._should_fix_namespace(using_namespace, defined_ns):
                    self.fixed_usings.append((using_namespace, defined_ns))
                    replacements.append((name_node.start_byte, name_node.end_byte, defined_ns))
                    fixed = True
                    break
            
            if not fixed:
                self.failed_usings.append(using_namespace)
        
        # 应用修改
        if replacements:
            modified_code = bytearray(source_code_bytes)
            for start, end, new_text in sorted(replacements, reverse=True):
                modified_code[start:end] = new_text.encode('utf-8')
        else:
            modified_code = source_code_bytes
        
        # 写入修改后的文件
        relative_path = os.path.relpath(file_path, start=input_dir)
        output_file_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'wb') as f:
            f.write(modified_code)

    def _should_fix_namespace(self, using_namespace, defined_ns):
        using_lower = using_namespace.lower()
        defined_lower = defined_ns.lower()
        
        return (defined_lower == using_lower and defined_ns != using_namespace) or \
               defined_lower.endswith(using_lower) or \
               (using_lower in defined_lower and defined_lower.startswith(using_lower + "."))

    def _copy_non_csharp_file(self, file_path, input_dir, output_dir):
        relative_path = os.path.relpath(file_path, start=input_dir)
        output_file_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        shutil.copy2(file_path, output_file_path)

    def process_directory(self, input_dir, output_dir):
        """
        处理指定目录中的所有C#文件
        
        Args:
            input_dir (str): 输入目录路径
            output_dir (str): 输出目录路径
        """
        # 收集所有命名空间和类型
        print("Collecting namespaces and types...")
        defined_namespaces, defined_types = self.collect_namespaces_and_types(input_dir)
        print(f"Collected {len(defined_namespaces)} namespaces and {len(defined_types)} types.\n")
        
        # 清理并创建输出目录
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # 处理所有文件
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".cs"):
                    self._process_csharp_file(file_path, input_dir, output_dir, defined_namespaces, defined_types)
                else:
                    self._copy_non_csharp_file(file_path, input_dir, output_dir)
        
        # 输出处理结果
        self._print_summary()

    def _print_summary(self):
        print("\n--- Using Directives Processing Summary ---\n")
        total_checked = len(self.successful_usings) + len(self.fixed_usings) + len(self.failed_usings)
        print(f"Total 'using' directives checked: {total_checked}")
        print(f"Successfully verified 'using' directives: {len(self.successful_usings)}")
        
        if self.fixed_usings:
            print(f"\nFixed 'using' directives ({len(self.fixed_usings)}):")
            for original, fixed in self.fixed_usings:
                print(f"  - using {original} => using {fixed}")
        
        if self.failed_usings:
            print(f"\n'using' directives that could not be fixed ({len(self.failed_usings)}):")
            for ns in self.failed_usings:
                print(f"  - Namespace or Type '{ns}' not found.")
        
        print("\n--- End of Summary ---\n")