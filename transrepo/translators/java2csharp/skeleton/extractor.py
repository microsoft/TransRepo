import argparse
import warnings
import os
from pathlib import Path
from typing import List
from tree_sitter import Parser, Tree
from tree_sitter_languages import get_language, get_parser
from core.utils.file_utils import FileUtils

from translators.java2csharp.skeleton.node_handler import JavaNodeHandler
from translators.java2csharp.skeleton.utils import JavaFileProcessor

class SkeletonExtractor:
    def __init__(self):
        warnings.filterwarnings("ignore", category=FutureWarning)
        self.language = get_language("java")
        self.parser = get_parser("java")
        self.node_handler = JavaNodeHandler()
        self.file_processor = JavaFileProcessor()
        self.file_utils = FileUtils()

    def process_directory(self, input_dir: str, output_dir: str) -> None:
        output_dir_path = Path(output_dir)

        output_dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created output directory: {output_dir}\n")

        for root, _, files in os.walk(input_dir):
            relative_root = Path(root).relative_to(input_dir)
            destination_root = output_dir_path / relative_root
            destination_root.mkdir(parents=True, exist_ok=True)

            if relative_root != Path('.'):
                print(f"Created directory: {relative_root}")

            for file in files:
                file_path = Path(root) / file
                if file.endswith(".java"):
                    self._process_java_file(file_path, input_dir, output_dir)
                else:
                    self._copy_non_java_file(file_path, input_dir, output_dir)

    def _process_java_file(self, file_path: Path, input_dir: str, output_dir: str) -> None:
        """Process a single Java file"""

        # Read the Java source code using FileUtils
        source_code_bytes = self.file_utils.read_text_file(file_path)

        # Parse the Java code and modify it
        tree = self.parser.parse(source_code_bytes)
        modified_code = self.node_handler.modify_function_and_static_blocks(tree, source_code_bytes)

        # Write the modified Java code to the output directory
        relative_path = file_path.relative_to(input_dir)
        output_file_path = Path(output_dir) / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the modified content using FileUtils
        self.file_utils.write_text_file(output_file_path, modified_code.decode('utf-8'))

        print(f"Processed Java file: {relative_path}\n")

    def _copy_non_java_file(self, file_path: Path, input_dir: str, output_dir: str) -> None:
        """Copy non-Java files using FileUtils"""
        relative_path = file_path.relative_to(input_dir)
        output_file_path = Path(output_dir) / relative_path

        # Use FileUtils to copy the file
        self.file_utils.copy_file(file_path, output_file_path)

        print(f"Copied non-Java file: {relative_path}\n")

def main():
    arg_parser = argparse.ArgumentParser(
        description='Process Java files by replacing function bodies with simple return statements, '
                    'and copy other files to the output directory.'
    )
    arg_parser.add_argument('input_dir', type=str, help='Path to the input Java project directory')
    arg_parser.add_argument('output_dir', type=str, help='Path to the output directory for modified Java files and other files')

    args = arg_parser.parse_args()
    print(f"Starting processing...\nInput Directory: {args.input_dir}\nOutput Directory: {args.output_dir}\n")
    
    extractor = SkeletonExtractor()
    extractor.process_directory(args.input_dir, args.output_dir)
    print("\nProcessing completed successfully.")

if __name__ == "__main__":
    main()