import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from alive_progress import alive_bar

from core.utils.logging_utils import setup_logging
from core.utils.file_utils import FileUtils
from translators.java2csharp.prompt_template import TestPromptTemplates
from core.llm.cloudgpt_aoai import get_chat_completion

class TestTranslator:
    def __init__(self, input_path: Path, output_path: Path, log_file: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.log_file = log_file
        self.file_utils = FileUtils()
        setup_logging(log_file)

    def translate(self) -> None:
        logging.info("Starting translation process...")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output path: {self.output_path}")

        start_time = time.time()
        success_count = 0
        failure_count = 0
        failed_repos = []

        # get total file num
        total_files = 0
        repos = [repo for repo in self.input_path.iterdir() if repo.is_dir()]
        for repo_path in repos:
            json_file = repo_path / f"{repo_path.name}_test_info.json"
            if json_file.exists():
                data = self.file_utils.read_json_file(json_file)
                total_files += len(data.get('test_files', []))

        with alive_bar(total_files, title="Processing files", bar="blocks") as bar:
            for repo_path in repos:
                json_file = repo_path / f"{repo_path.name}_test_info.json"
                if json_file.exists():
                    result = self._process_repo(repo_path, json_file, bar)
                    if result:
                        success_count += 1
                    else:
                        failure_count += 1
                        failed_repos.append(repo_path.name)
                else:
                    logging.warning(f"JSON file not found for repository: {json_file}")
                    failure_count += 1
                    failed_repos.append(repo_path.name)

        end_time = time.time()
        self._log_results(success_count, failure_count, failed_repos, end_time - start_time)

    def _process_repo(self, repo_path: Path, json_file: Path, bar) -> bool:
        try:
            logging.info(f"Processing repository: {repo_path.name}")

            # Load component mappings using FileUtils
            component_mappings = self.file_utils.read_json_file(repo_path / 'java_to_csharp_mappings.json')

            # Load the test info JSON using FileUtils
            data = self.file_utils.read_json_file(json_file)
            test_files = data['test_files']
            success_count = 0
            
            for test_file in test_files:
                input_file = repo_path / test_file
                if self._process_file(input_file, component_mappings):
                    success_count += 1
                bar()

            return success_count == len(test_files)

        except Exception as e:
            logging.error(f"Error processing repository {repo_path.name}: {e}")
            return False

    def _process_file(self, input_file: Path, component_mappings: Dict[str, str]) -> bool:
        logging.info(f"Processing file: {input_file}")
        try:
            # Use FileUtils to read the Java test file
            java_content = self.file_utils.read_text_file(input_file)

            # Translate the Java file to C#
            csharp_content = self._translate_java_to_csharp(
                java_content, 
                input_file.name, 
                component_mappings
            )

            if csharp_content:
                rel_path = input_file.relative_to(self.input_path)
                output_file = self.output_path / rel_path.with_suffix('.cs')

                # Use FileUtils to write the translated C# file
                self.file_utils.write_text_file(output_file, csharp_content)
                
                logging.info(f"Successfully translated {input_file} to {output_file}")
                return True
            
            return False

        except Exception as e:
            logging.error(f"Error processing {input_file}: {e}")
            return False

    def _translate_java_to_csharp(self, java_content: str, file_name: str, component_mappings: Dict[str, str]) -> Optional[str]:
        logging.info(f"Translating {file_name}...")
        
        mappings_str = "\n".join(f"{java_comp} -> {cs_comp}" 
                                for java_comp, cs_comp in component_mappings.items())
        
        messages = [
            {
                "role": "system", 
                "content": TestPromptTemplates.get_system_message(mappings_str)
            },
            {
                "role": "user",
                "content": f"Please translate this Java test file to C#, only plain text is allowed, don't use markdown:\n\n{java_content}"
            }
        ]

        try:
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
            )
            logging.info(f"Translation of {file_name} completed successfully.")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Translation failed for {file_name}: {e}")
            return None

    def _log_results(self, success_count: int, failure_count: int, failed_repos: List[str], total_time: float) -> None:
        logging.info(f"Processing completed. Success: {success_count}, Failures: {failure_count}")
        logging.info(f"Total time taken: {total_time:.2f} seconds")
        
        if failed_repos:
            logging.info("The following repositories failed:")
            for repo in failed_repos:
                logging.info(f"- {repo}")
        else:
            logging.info("All repositories have been successfully processed.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate Java test files to C#")
    parser.add_argument("--input_path", type=Path, required=True, help="Path to the directory containing repository folders")
    parser.add_argument("--output_path", type=Path, required=True, help="Path to save the translated C# files")
    parser.add_argument("--log_file", type=Path, required=True, help="Path to log file")

    args = parser.parse_args()
    translator = TestTranslator(args.input_path, args.output_path, args.log_file)
    translator.translate()

if __name__ == "__main__":
    main()