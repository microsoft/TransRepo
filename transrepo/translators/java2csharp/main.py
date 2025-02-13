import argparse
import logging
from pathlib import Path
from core.utils.logging_utils import setup_logging

from translators.java2csharp.pre_proc.java2csharp_mapper import JavaToCSharpMapper
# from translators.java2csharp.skeleton.extractor import SkeletonExtractor
from translators.java2csharp.skeleton_translator import SkeletonTranslator
from translators.java2csharp.skeleton.skeleton_extractor import JavaSkeletonExtractor
from translators.java2csharp.ci_translator import CITranslator
from translators.java2csharp.test_translator import TestTranslator
from translators.java2csharp.post_proc.namespace_fixer import NamespaceFixer
from translators.java2csharp.post_proc.auto_build import RepoBuilder
from translators.java2csharp.post_proc.modify_csproj import CsprojModifier


def main(args):
    # Define the log directory and log file based on the input log_id
    log_dir = Path("../../../../log")
    log_dir.mkdir(parents=True, exist_ok=True)  # Create the log directory if it doesn't exist
    log_file = log_dir / f"{args.log_id}.log"

    # Set up logging
    setup_logging(log_file)

    try:
        # Step 1: Use JavaToCSharpMapper to map Java components to C# equivalents
        logging.info("Step 1: Translating Java components to C# equivalents...")
        translator = JavaToCSharpMapper(Path(args.java_input_dir))
        translator.process_all_repositories()
        logging.info(f"Java to C# component mapping completed for {args.java_input_dir}")

        # Step 2: Run SkeletonExtractor to extract the Java project's skeleton
        logging.info("Step 2: Extracting Java skeletons...")
        processor = JavaSkeletonExtractor(args.java_input_dir, args.java_skeleton_dir)
        logging.info(f"Java skeleton extracted to {args.java_skeleton_dir}")
        processor.process_java_directory()

        # Step 3: Run SkeletonTranslator to perform Java -> C# skeleton translation
        logging.info("Step 3: Translating skeleton to C#...")
        skeleton_translator = SkeletonTranslator(
            input_path=Path(args.java_skeleton_dir),
            output_path=Path(args.csharp_output_dir),
            log_file=log_file
        )
        skeleton_translator.translate()
        logging.info(f"C# skeleton translated to {args.csharp_output_dir}")

        # Step 4: Run CITranslator to handle CI translations
        logging.info("Step 4: Translating CI...")
        ci_translator = CITranslator(
            input_jsonl=Path(args.ci_input_jsonl),
            cache_dir=Path(args.java_input_dir),
            output_dir=Path(args.csharp_output_dir),
            log_file=log_file
        )
        ci_translator.translate()
        logging.info(f"CI translation completed and saved to {args.csharp_output_dir}")

        # Step 5: Run TestTranslator to handle test case translation
        logging.info("Step 5: Translating test cases...")
        test_translator = TestTranslator(
            input_path=Path(args.java_input_dir),
            output_path=Path(args.csharp_output_dir),
            log_file=log_file
        )
        test_translator.translate()
        logging.info(f"Test cases translation completed and saved to {args.csharp_output_dir}")

        # Step 6: Run NamespaceFixer to process and fix namespaces in C# files
        logging.info("Step 6: Fixing namespaces and processing C# files...")
        namespace_fixer = NamespaceFixer()
        namespace_fixer.process_directory(args.csharp_output_dir, args.csharp_final_dir)
        logging.info(f"Namespace fixing completed and saved to {args.csharp_final_dir}")

        # Step 7: Process all repos to configure solutions and projects
        logging.info("Step 7: Configuring solutions and projects...")
        repo_processor = RepoBuilder(args.csharp_final_dir, args.ci_input_jsonl, log_file=log_file)
        repo_processor.process_all_repos()
        logging.info("Repo processing and project configuration completed.")

        # Step 8: Modify all .csproj files based on java_to_csharp_mappings.json
        logging.info("Step 8: Modifying .csproj files based on java_to_csharp_mappings.json...")
        csproj_modifier = CsprojModifier(cache_dir=args.csharp_final_dir, log_file=log_file)
        csproj_modifier.process_all_repos()
        logging.info(".csproj modification completed.")

        logging.info("All steps completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred during the translation process: {e}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="One-stop script for Java to C# translation process.")
    
    parser.add_argument("--java_input_dir", type=str, required=True, 
                        help="Path to the input directory containing Java source code.")
    parser.add_argument("--java_skeleton_dir", type=str, required=True, 
                        help="Path to the output directory for Java skeleton extraction.")
    parser.add_argument("--csharp_output_dir", type=str, required=True, 
                        help="Path to the output directory for C# skeleton translation.")
    parser.add_argument("--csharp_final_dir", type=str, required=True, 
                        help="Path to the output directory for C# final translation.")
    parser.add_argument("--ci_input_jsonl", type=str, required=True, 
                        help="Path to the input JSONL file for CI and test case translation.")
    parser.add_argument("--log_id", type=str, required=True, 
                        help="Unique identifier for the log file.")

    args = parser.parse_args()

    main(args)
"""
python3 main.py --java_input_dir /home/v-jiahengwen/RepoTranslationAgent/data/java/simple_repo \
--java_skeleton_dir /home/v-jiahengwen/RepoTranslationAgent/output/skeleton/java/mini_repo2 \
--csharp_output_dir /home/v-jiahengwen/RepoTranslationAgent/output/skeleton/c_sharp/mini_repo2 \
--csharp_final_dir /home/v-jiahengwen/RepoTranslationAgent/output/skeleton/c_sharp/mini_repo2_final \
--ci_input_jsonl /home/v-jiahengwen/RepoTranslationAgent/data/java/simple_repo/test_ci.jsonl \
--log_id test03
"""