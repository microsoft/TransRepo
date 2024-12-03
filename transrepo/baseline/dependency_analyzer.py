from tree_sitter import Language, Parser
import os
from collections import defaultdict
from tqdm import tqdm
from pathlib import Path

class DependencyAnalyzer:
    def __init__(self):
        # Load Java language for tree-sitter
        self.java_language = Language('./build/my-languages.so', 'java')
        self.parser = Parser()
        self.parser.set_language(self.java_language)

    def analyze_project(self, project_path: Path, output_path: Path):
        """分析项目依赖关系并生成依赖文件"""
        project_dependencies, method_definitions, method_usage = self._analyze_project_structure(project_path)
        self._save_dependency_analysis(
            project_path,
            project_path.name,
            project_dependencies,
            method_definitions,
            method_usage,
            output_path
        )
        
    def _parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        return self.parser.parse(bytes(code, 'utf8')).root_node

    def _collect_definitions(self, root_node):
        query = self.java_language.query('''
        (
          (method_declaration
            name: (identifier) @method-name)
        )
        ''')
        captures = query.captures(root_node)
        definitions = {}

        for capture in captures:
            method_name = capture[0].text.decode()
            definitions[method_name] = capture[0].start_point

        return definitions

    def _collect_dependencies(self, root_node):
        query = self.java_language.query('''
        (
          (method_invocation
            object: (identifier) @class-name
            name: (identifier) @method-name)
        )
        ''')
        captures = query.captures(root_node)
        dependencies = set()

        class_name = ''
        for capture in captures:
            node_type = capture[1]
            if node_type == 'class-name':
                class_name = capture[0].text.decode()
            elif node_type == 'method-name':
                method_name = capture[0].text.decode()
                dependencies.add((class_name, method_name))

        return dependencies

    def _analyze_project_structure(self, directory):
        project_dependencies = {}
        method_definitions = {}
        method_usage = defaultdict(set)

        java_files = list(directory.rglob('*.java'))

        # First pass: Collect method definitions
        for file_path in tqdm(java_files, desc="Collecting definitions"):
            root_node = self._parse_file(file_path)
            definitions = self._collect_definitions(root_node)
            for method, location in definitions.items():
                method_definitions[method] = file_path

        # Second pass: Collect dependencies
        for file_path in tqdm(java_files, desc="Collecting dependencies"):
            root_node = self._parse_file(file_path)
            dependencies = self._collect_dependencies(root_node)
            project_dependencies[file_path] = dependencies

            for _, method_name in dependencies:
                method_usage[method_name].add(file_path)

        return project_dependencies, method_definitions, method_usage

    def _save_dependency_analysis(self, project_path, project_name, project_dependencies, 
                                method_definitions, method_usage, output_path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Project: {project_name}\n")
            for file_path, deps in project_dependencies.items():
                file_name = file_path.name
                f.write(f"File: {file_name}\n")
                for class_name, method_name in deps:
                    defined_in = method_definitions.get(method_name, "Unknown")
                    defined_file_name = defined_in.name if isinstance(defined_in, Path) else "Unknown"
                    f.write(f"Calls: {class_name}.{method_name} (Defined in: {defined_file_name})\n")

def main():
    projects_directory = Path(r'RepoTranslationAgent/data/java/hutool-test')
    output_directory = Path(r'RepoTranslationAgent/data/cs/hutool-test')
    
    analyzer = DependencyAnalyzer()
    
    for project_path in projects_directory.iterdir():
        if project_path.is_dir():
            output_path = output_directory / project_path.name / f"{project_path.name}_dependency_analysis.txt"
            analyzer.analyze_project(project_path, output_path)

if __name__ == "__main__":
    main()