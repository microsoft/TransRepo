import os
import json
from pathlib import Path
from core.llm.cloudgpt_aoai import get_chat_completion

class JavaToCSharpMapper:
    def __init__(self, repos_base_path: Path):
        self.repos_base_path = repos_base_path

    def find_java_files(self, repo_path: Path) -> list:
        """Find all Java files in the repository."""
        java_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))
        return java_files

    def read_file_content(self, file_path: Path) -> str:
        """Read the content of a file with fallback for encoding issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin1') as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                return ""

    def extract_java_components(self, file_content: str) -> list:
        """Extract Java components using an LLM."""
        prompt = f"""
        Analyze the following Java code and list all Java-specific components:
        1. All imported packages
        2. Base classes being extended
        3. Interfaces being implemented
        4. Java-specific classes and interfaces being used
        5. Java UI components (if any)
        
        Return ONLY the component list, one per line.
        Code to analyze:
        {file_content}
        """
        messages = [{"role": "user", "content": prompt}]
        try:
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
            )
            components = response.choices[0].message.content.strip().split('\n')
            components = [comp.strip() for comp in components if comp.strip()]
            return components
        except Exception as e:
            print(f"Error in extract_java_components: {str(e)}")
            return []

    def find_csharp_equivalents(self, components: list) -> dict:
        """Map Java components to their C# equivalents using an LLM."""
        if not components:
            print("No components to map")
            return {}
        
        components_list = '\n'.join([c for c in components if c.startswith(('java.', 'javax.', 'org.junit'))])
        prompt = (
            "As a software development expert, map each Java component to its C# equivalent.\n"
            "Please map these Java components:\n"
            + components_list +
            "\nRespond ONLY with the mappings in the format: \"JavaComponent -> C#Component\""
        )

        messages = [{"role": "user", "content": prompt}]
        try:
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
                temperature=0.2
            )
            mappings = {}
            for line in response.choices[0].message.content.strip().split('\n'):
                line = line.strip()
                if '->' in line:
                    java_comp, csharp_comp = map(str.strip, line.split('->'))
                    mappings[java_comp] = csharp_comp
            return mappings
        except Exception as e:
            print(f"Error in find_csharp_equivalents: {str(e)}")
            return {}

    def process_repository(self, repo_path: Path):
        """Process a single repository and map Java components to C# equivalents."""
        java_files = self.find_java_files(repo_path)
        print(f"Found {len(java_files)} Java files in {repo_path.name}")

        all_components = set()
        for file_path in java_files:
            content = self.read_file_content(file_path)
            if content:
                components = self.extract_java_components(content)
                all_components.update(components)

        if all_components:
            mappings = self.find_csharp_equivalents(list(all_components))
            
            # save mapping file
            output_file = repo_path / 'java_to_csharp_mappings.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, indent=4, ensure_ascii=False)
            print(f"Generated mapping file: {output_file}")
        else:
            print(f"No Java components found in repository {repo_path}")

    def process_all_repositories(self):
        """Process all repositories in the base path."""
        for item in self.repos_base_path.iterdir():
            if item.is_dir():
                print(f"\nProcessing repository: {item.name}")
                self.process_repository(item)