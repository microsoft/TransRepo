import json
import logging
from pathlib import Path
from typing import List
from alive_progress import alive_bar

from core.utils.logging_utils import setup_logging
from core.utils.file_utils import FileUtils
from translators.java2csharp.prompt_template import CIPromptTemplates
from core.llm.cloudgpt_aoai import get_chat_completion

class CITranslator:
    def __init__(self, input_jsonl: Path, cache_dir: Path, output_dir: Path, log_file: Path):
        self.input_jsonl = input_jsonl
        self.cache_dir = cache_dir
        self.output_dir = output_dir
        self.log_file = log_file
        self.file_utils = FileUtils()
        setup_logging(log_file)

    def translate(self) -> None:
        logging.info(f"Reading input JSONL file: {self.input_jsonl}")
        try:
            instances = self.file_utils.read_jsonl(self.input_jsonl)
        except Exception as e:
            logging.error(f"Failed to read input JSONL: {e}")
            return

        logging.info(f"Total instances to process: {len(instances)}")
        success_count = 0
        failure_count = 0
        failed_instances = []

        with alive_bar(len(instances), title="Processing instances", bar="blocks") as bar:
            for instance in instances:
                result = self._process_instance(instance)
                if result:
                    success_count += 1
                else:
                    failure_count += 1
                    failed_instances.append(instance.get("instance_id", "Unknown"))
                bar()

        self._log_results(success_count, failure_count, failed_instances)

    def _process_instance(self, instance: dict) -> bool:
        instance_id = instance.get("instance_id")
        if not self._validate_instance(instance):
            return False

        try:
            ci_file_path = self.cache_dir / instance_id / instance["ci_file"]
            with ci_file_path.open('r', encoding='utf-8') as f:
                ci_content = f.read()

            translated_content = self._get_translation(ci_content, instance_id)
            if not translated_content:
                return False

            self.file_utils.write_ci_file(
                instance_id, 
                translated_content, 
                self.output_dir, 
                instance["ci_file"]
            )
            logging.info(f"CI file for instance {instance_id} has been translated and saved.")
            return True

        except Exception as e:
            logging.error(f"Error processing instance {instance_id}: {e}")
            return False

    def _validate_instance(self, instance: dict) -> bool:
        instance_id = instance.get("instance_id")
        if not instance_id:
            logging.warning("Missing instance_id, skipping this instance.")
            return False

        repo_path = self.cache_dir / instance_id
        if not repo_path.exists():
            logging.warning(f"Repository path {repo_path} does not exist.")
            return False

        ci_file_rel = instance.get("ci_file")
        if not ci_file_rel:
            logging.warning(f"Instance {instance_id} is missing ci_file field.")
            return False

        return True



    def _process_llm_response(self, response_content: str, instance_id: str) -> str:
        """deal with LLM response"""
        logging.debug(f"Raw response for {instance_id}: {response_content}")
        
        try:
            response_json = json.loads(response_content)
            translated_ci = response_json.get("translated_ci")
            if translated_ci:
                return translated_ci
        except json.JSONDecodeError:
            pass
        
        cleaned_content = response_content.strip()
        
        # search for json start loc
        json_start = cleaned_content.find('{')
        if json_start == -1:
            logging.error(f"No JSON object found in response for {instance_id}")
            return None
            
        # search for json end loc
        json_end = cleaned_content.rfind('}') + 1
        if json_end <= json_start:
            logging.error(f"Invalid JSON structure in response for {instance_id}")
            return None
            
        # extract json content
        json_content = cleaned_content[json_start:json_end]
        
        try:
            response_json = json.loads(json_content)
        except json.JSONDecodeError as je:
            logging.error(f"JSON parsing error for {instance_id}: {je}")
            logging.error(f"Attempted to parse: {json_content}")
            return None
            
        translated_ci = response_json.get("translated_ci")
        if not translated_ci:
            logging.error(f"No translated_ci field in response for {instance_id}")
            return None
            
        return translated_ci

    def _get_translation(self, ci_content: str, instance_id: str) -> str:
        prompt = CIPromptTemplates.get_ci_translation_prompt(ci_content, instance_id)
        messages = [
            {"role": "system", "content": CIPromptTemplates.get_system_message()},
            {"role": "user", "content": prompt}
        ]

        try:
            response = get_chat_completion(
                engine="gpt-4o-20240513",
                messages=messages,
            )
            
            if not response or not response.choices:
                logging.error(f"Empty or invalid API response for {instance_id}")
                return None

            response_content = response.choices[0].message.content
            return self._process_llm_response(response_content, instance_id)
            
        except Exception as e:
            logging.error(f"Translation failed for {instance_id}: {str(e)}")
            logging.error(f"Full error: {e.__class__.__name__}: {str(e)}")
            return None

    def _log_results(self, success_count: int, failure_count: int, failed_instances: List[str]) -> None:
        logging.info(f"Processing completed. Success: {success_count}, Failures: {failure_count}")
        if failed_instances:
            logging.info("The following instances failed:")
            for fid in failed_instances:
                logging.info(f"- {fid}")
        else:
            logging.info("All instances have been successfully processed.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate Java Repo CI files to C# project CI files")
    parser.add_argument("--input_jsonl", type=Path, required=True, help="Path to input JSONL file")
    parser.add_argument("--cache_dir", type=Path, required=True, help="Path to cache directory where Java Repos are stored")
    parser.add_argument("--output_dir", type=Path, required=True, help="Path to output directory")
    parser.add_argument("--log_file", type=Path, required=True, help="Path to log file")

    args = parser.parse_args()
    translator = CITranslator(args.input_jsonl, args.cache_dir, args.output_dir, args.log_file)
    translator.translate()

if __name__ == "__main__":
    main()