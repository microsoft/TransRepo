import os
import json
import logging
from pathlib import Path
from core.llm.cloudgpt_aoai import get_chat_completion
from core.utils.file_utils import FileUtils
from typing import List, Tuple, Dict


class CsprojModifier:
    def __init__(self, cache_dir, log_file):
        self.cache_dir = Path(cache_dir)
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(levelname)s:%(message)s')

    def generate_prompt(self, csproj_files: List[Tuple[str, str]], mapping_content, instance_id):
        """
        Generates a prompt for the LLM based on multiple .csproj contents and mapping content. 
        """
        prompt = f"""
    You are an expert in both Java and C#. I have multiple C# project files (`.csproj`) that I need you to modify based on some mappings we have from a Java project to a C# project.

    Here are the C# project files content:

    """
        # Add each csproj file content to the prompt
        for i, (file_path, content) in enumerate(csproj_files):
            prompt += f"[File {i+1}: {Path(file_path).name}]\n```xml\n{content}\n```\n\n"

        prompt += f"""
    And here are the mappings from the Java project to the C# project, which specify the C# components and libraries to use:
    {json.dumps(mapping_content, indent=2)}

    Please modify all C# project files (.csproj) for .NET 8.0 projects using NUnit test framework. Ensure that:

    1.The correct NUnit packages are referenced:
        NUnit (core framework)
        NUnit3TestAdapter (for test discovery and execution)
        Microsoft.NET.Test.Sdk (required for running tests)
        FluentAssertions (recommended for better assertions)
    2.Project dependencies are correctly configured
    3.The XML format is valid and properly formatted
    4.The project targets .NET 8.0 with proper configurations:
        ImplicitUsings enabled
        Nullable enabled
        Remove any redundant package references that are already included in .NET 8.0 runtime
    5.Package versions are consistent across all projects
    6.Dependencies between projects are properly configured

    Return the modified content for all .csproj files in the following JSON format:
    {
        "files": [
            {
                "content": "modified content for first file"
            },
            {
                "content": "modified content for second file"
            }
        ]
    }
    """
        return prompt

    def run_llm_for_modification(self, csproj_files: List[Tuple[str, str]], mapping_content, instance_id):
        """Invoke LLM to generate modification suggestions for multiple .csproj files."""
        prompt = self.generate_prompt(csproj_files, mapping_content, instance_id)
        messages = [
            {"role": "system", "content": "You are an expert in C# and Java project configurations."},
            {"role": "user", "content": prompt}
        ]

        try:
            # Call LLM to modify the .csproj files
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
            )
            response_content = response.choices[0].message.content
            
            logging.info(f"Modified content for {instance_id}:\n{response_content}")

            start = response_content.find('{')
            end = response_content.rfind('}') + 1
            if start == -1 or end <= start:
                logging.error(f"Invalid JSON format in response for {instance_id}")
                return None

            json_content = response_content[start:end]
            modified_contents = json.loads(json_content)

            if not isinstance(modified_contents, dict) or 'files' not in modified_contents:
                logging.error(f"Invalid response format for {instance_id}")
                return None

            files = modified_contents['files']
            if len(files) != len(csproj_files):
                logging.error(f"Number of files in response ({len(files)}) doesn't match input ({len(csproj_files)})")
                return None

            for i, file in enumerate(files):
                content = file.get('content', '')
                if not ("<Project" in content and "</Project>" in content):
                    logging.error(f"Invalid csproj XML in response for file {i}")
                    return None

            return files

        except Exception as e:
            logging.error(f"Error while modifying .csproj using LLM for instance {instance_id}: {e}")
            return None

    def process_repo(self, repo_dir, instance_id):
        """Process a single repository, find its .csproj files and modify them based on the mapping file."""
        try:
            # Locate the mapping file
            mapping_path = Path(repo_dir) / 'java_to_csharp_mappings.json'

            if not mapping_path.exists():
                logging.warning(f"Mapping file not found in {repo_dir}: {mapping_path}")
                return

            mapping_content = FileUtils.read_json_file(mapping_path)

            csproj_files = []
            for root, _, files in os.walk(repo_dir):
                for file in files:
                    if file.endswith('.csproj'):
                        file_path = os.path.join(root, file)
                        content = FileUtils.read_text_file(Path(file_path))
                        csproj_files.append((file_path, content))

            if not csproj_files:
                logging.info(f"No .csproj files found in {repo_dir}")
                return

            modified_files = self.run_llm_for_modification(csproj_files, mapping_content, instance_id)

            if modified_files:
                for (file_path, _), modified_file in zip(csproj_files, modified_files):
                    modified_content = modified_file['content']
                    FileUtils.write_text_file(Path(file_path), modified_content)
                    logging.info(f"Modified .csproj file: {file_path}")
            else:
                logging.warning(f"No modifications made to files in {repo_dir}")

        except Exception as e:
            logging.error(f"Error processing repository {repo_dir} for instance {instance_id}: {e}")

    def process_all_repos(self):
        """Iterate over all directories in cache_dir and process their .csproj files."""
        try:
            # Iterate through all subdirectories in cache_dir
            for repo_dir in self.cache_dir.iterdir():
                if repo_dir.is_dir():
                    instance_id = repo_dir.name
                    logging.info(f"Processing repository: {repo_dir}")
                    self.process_repo(repo_dir, instance_id)
                else:
                    logging.warning(f"Skipping non-directory item in cache_dir: {repo_dir}")
        except Exception as e:
            logging.error(f"Error processing repositories in {self.cache_dir}: {e}")


if __name__ == "__main__":
    cache_dir = "/path/to/your/cache_dir"
    log_file = "csproj_modifier.log"

    modifier = CsprojModifier(cache_dir, log_file)
    modifier.process_all_repos()
