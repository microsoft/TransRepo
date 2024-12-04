import json
import logging
from pathlib import Path
from typing import Dict, Optional
from alive_progress import alive_bar

from core.utils.logging_utils import setup_logging
from core.utils.file_utils import FileUtils
from core.llm.cloudgpt_aoai import get_chat_completion
from translators.java2csharp.prompt_template import SkeletonPromptTemplates

class SkeletonTranslator:
    def __init__(self, input_path: Path, output_path: Path, log_file: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.log_file = log_file
        self.file_utils = FileUtils()
        setup_logging(log_file)

    def translate(self) -> None:
        logging.info(f"Starting skeleton translation process")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output path: {self.output_path}")

        repos = [p for p in self.input_path.iterdir() if p.is_dir()]
        
        total_files = 0
        for repo_path in repos:
            java_files = list(repo_path.rglob("*.java"))
            other_files = [p for p in repo_path.rglob("*") if p.is_file() and p.suffix != '.java']
            total_files += len(java_files) + len(other_files)

        with alive_bar(total_files, title="Processing repositories and files", bar="blocks") as bar:
            for repo_path in repos:
                self._process_repo(repo_path, bar)

        logging.info("All repositories processed. Translation completed.")

    def _process_repo(self, repo_path: Path, bar) -> None:
        logging.info(f"\nProcessing repository: {repo_path.name}")
        
        component_mappings = self.file_utils.read_json_file(repo_path / 'java_to_csharp_mappings.json')
        repo_output_path = self.output_path / repo_path.name
        
        java_files = list(repo_path.rglob("*.java"))
        other_files = [p for p in repo_path.rglob("*") if p.is_file() and p.suffix != '.java']
        
        logging.info(f"Found {len(java_files)} Java files and {len(other_files)} other files")

        # Process Java files
        for java_file in java_files:
            self._process_java_file(java_file, repo_path, repo_output_path, component_mappings)
            bar()

        # Copy other files
        for other_file in other_files:
            self._copy_non_java_file(other_file, repo_path, repo_output_path)
            bar()

    def _process_java_file(self, java_file: Path, repo_path: Path, repo_output_path: Path, component_mappings: Dict) -> None:
        try:
            java_content = self.file_utils.read_text_file(java_file)
            cs_content = self._translate_java_to_cs(java_content, java_file.name, component_mappings)
            
            if cs_content:
                # calculate path relative to repo_path，then get repo_output_path
                relative_path = java_file.relative_to(repo_path)
                output_file = repo_output_path / relative_path.with_suffix('.cs')
                self.file_utils.write_text_file(output_file, cs_content)
                logging.info(f"Successfully translated: {java_file.name}")
            else:
                logging.error(f"Failed to translate: {java_file.name}")
        
        except Exception as e:
            logging.error(f"Error processing {java_file}: {e}")

    def _copy_non_java_file(self, source_file: Path, repo_path: Path, repo_output_path: Path) -> None:
        try:
            # calculate path relative to repo_path，then get repo_output_path
            relative_path = source_file.relative_to(repo_path)
            output_file = repo_output_path / relative_path
                
            # make sure output dir exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            self.file_utils.copy_file(source_file, output_file)
        except Exception as e:
            logging.error(f"Error copying {source_file} to {output_file}: {e}")

    def _translate_java_to_cs(self, java_content: str, file_name: str, component_mappings: Dict) -> Optional[str]:
        mappings_str = "\n".join([f"{java_comp} -> {cs_comp}" 
                                 for java_comp, cs_comp in component_mappings.items()])
        
        messages = [
            {
                "role": "system",
                "content": SkeletonPromptTemplates.get_system_message(mappings_str)
            },
            {
                "role": "user",
                "content": java_content
            }
        ]

        try:
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Translation failed for {file_name}: {e}")
            return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate Java skeleton files to C# and copy non-Java files")
    parser.add_argument("--input_path", type=Path, required=True, 
                       help="Path to the directory containing multiple Java repos")
    parser.add_argument("--output_path", type=Path, required=True,
                       help="Path to save the translated C# files and copied non-Java files")
    parser.add_argument("--log_file", type=Path, required=True,
                       help="Path to log file")

    args = parser.parse_args()
    translator = SkeletonTranslator(args.input_path, args.output_path, args.log_file)
    translator.translate()

if __name__ == "__main__":
    main()