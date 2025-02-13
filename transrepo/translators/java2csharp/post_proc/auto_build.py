import os
import json
import subprocess
import logging
from collections import defaultdict

class RepoBuilder:
    def __init__(self, cache_dir, input_jsonl, log_file):
        self.cache_dir = cache_dir
        self.input_jsonl = input_jsonl
        self.log_file = log_file

    def run_command(self, command, repo_dir):
        """Run a shell command in the specified directory."""
        try:
            logging.info(f"Running command: {' '.join(command)} in {repo_dir}")
            result = subprocess.run(
                command,
                cwd=repo_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"Command output: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Command '{' '.join(command)}' failed with error: {e}")
            logging.error(f"Error details: {e.stderr.strip()}")

    def ensure_directory_exists(self, directory):
        """Ensure the directory exists, and if not, create it."""
        if not os.path.exists(directory):
            logging.info(f"Creating directory: {directory}")
            os.makedirs(directory)

    def is_project_in_solution(self, solution_path, project_path):
        """Check if the project is already included in the solution."""
        try:
            result = subprocess.run(
                ["dotnet", "sln", solution_path, "list"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            normalized_project_path = os.path.abspath(project_path)
            for line in result.stdout.splitlines():
                project_full_path = os.path.abspath(os.path.join(os.path.dirname(solution_path), line.strip()))
                if project_full_path == normalized_project_path:
                    return True
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to list projects in solution: {e.stderr.strip()}")
            return False

    def split_test_and_non_test(self, all_cs_files, test_files):
        """Split files into test and non-test groups based on provided test_files."""
        test_set = set(test_files)
        test_paths = [path for path in all_cs_files if path in test_set]
        non_test_paths = [path for path in all_cs_files if path not in test_set]
        return test_paths, non_test_paths

    def build_tree(self, paths, root):
        """Build a tree from the list of paths."""
        tree = {}
        for path in paths:
            parts = os.path.relpath(path, root).split(os.sep)
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        return tree

    def traverse_and_collect(self, tree, current_path, group_roots, repo_dir):
        """
        Traverse the tree and collect group roots by merging single child directories.
        If a directory has multiple children or is a leaf, mark it as a group root and do not traverse further.
        If a directory has only one child, continue traversing.
        """
        if not tree:
            group_roots.append(current_path)
            return

        if len(tree) > 1:
            group_roots.append(current_path)
            return
        elif len(tree) == 1:
            subdir = next(iter(tree))
            self.traverse_and_collect(tree[subdir], os.path.join(current_path, subdir), group_roots, repo_dir)
        else:
            group_roots.append(current_path)
            return

    def merge_single_child_directories(self, dirs, repo_dir):
        """Merge directories that have only one child up to the highest possible directory."""
        tree = self.build_tree(dirs, repo_dir)
        group_roots = []
        self.traverse_and_collect(tree, repo_dir, group_roots, repo_dir)

        final_group_roots = []
        sorted_roots = sorted(group_roots, key=lambda x: len(x.split(os.sep)), reverse=True)
        for root in sorted_roots:
            if not any(os.path.commonpath([root, existing]) == existing for existing in final_group_roots):
                final_group_roots.append(root)

        return final_group_roots

    def generate_unique_project_name(self, repo_dir, directory):
        """Generate a unique project name based on the directory's relative path."""
        relative_path = os.path.relpath(directory, repo_dir)
        project_name = relative_path.replace(os.sep, '_').replace('.', '_')
        return project_name

    def modify_csproj(self, csproj_path):
        """Add ProduceReferenceAssembly setting to csproj file."""
        try:
            with open(csproj_path, 'r') as f:
                content = f.read()

            if '<PropertyGroup>' in content and '<ProduceReferenceAssembly>false</ProduceReferenceAssembly>' not in content:
                modified_content = content.replace(
                    '<PropertyGroup>',
                    '<PropertyGroup>\n    <ProduceReferenceAssembly>false</ProduceReferenceAssembly>'
                )
                with open(csproj_path, 'w') as f:
                    f.write(modified_content)
                logging.info(f"Added ProduceReferenceAssembly setting to {csproj_path}")
        except Exception as e:
            logging.error(f"Error modifying csproj file {csproj_path}: {e}")

    def create_solution_and_projects(self, repo_dir, test_dirs, non_test_dirs):
        """Create solution file and add projects based on test and non-test directories."""
        solution_name = os.path.basename(repo_dir)
        solution_path = os.path.join(repo_dir, f"{solution_name}.sln")
        if not os.path.exists(solution_path):
            logging.info(f"Creating solution: {solution_name}")
            self.run_command(["dotnet", "new", "sln", "-n", solution_name], repo_dir)
        else:
            logging.info(f"Solution {solution_name}.sln already exists.")

        non_test_projects = {}
        for directory in non_test_dirs:
            project_name = self.generate_unique_project_name(repo_dir, directory)
            csproj_path = os.path.join(directory, f"{project_name}.csproj")

            self.ensure_directory_exists(directory)

            if not os.path.exists(csproj_path):
                logging.info(f"Creating Class Library project: {project_name} in {directory}")
                self.run_command(["dotnet", "new", "classlib", "-n", project_name, "-o", "."], directory)
                self.modify_csproj(csproj_path)
            else:
                logging.info(f"Project {csproj_path} already exists, skipping creation.")
                self.modify_csproj(csproj_path)

            if not self.is_project_in_solution(solution_path, csproj_path):
                self.run_command(["dotnet", "sln", "add", csproj_path], repo_dir)
            non_test_projects[project_name] = csproj_path

        test_projects = []
        for directory in test_dirs:
            project_name = self.generate_unique_project_name(repo_dir, directory)
            csproj_path = os.path.join(directory, f"{project_name}.csproj")

            self.ensure_directory_exists(directory)

            if not os.path.exists(csproj_path):
                logging.info(f"Creating NUnit project: {project_name} in {directory}")
                self.run_command(["dotnet", "new", "nunit", "-n", project_name, "-o", "."], directory)
                self.modify_csproj(csproj_path)
            else:
                logging.info(f"Project {csproj_path} already exists, skipping creation.")
                self.modify_csproj(csproj_path)

            if not self.is_project_in_solution(solution_path, csproj_path):
                self.run_command(["dotnet", "sln", "add", csproj_path], repo_dir)
            test_projects.append((project_name, csproj_path))

        for test_project_name, test_proj_path in test_projects:
            for non_test_proj_name, non_test_proj_path in non_test_projects.items():
                logging.info(f"Adding reference from {test_proj_path} to {non_test_proj_path}")
                self.run_command(["dotnet", "add", test_proj_path, "reference", non_test_proj_path], repo_dir)

    def process_repo(self, repo_dir, instance_data):
        """Process a single repo to configure the solution and projects."""
        test_files = [test_file.replace(".java", ".cs") for test_file in instance_data.get('test_file', [])]
        test_files = [os.path.abspath(os.path.join(repo_dir, test_file)) for test_file in test_files]
        test_files = [f for f in test_files if os.path.commonpath([repo_dir, f]) == repo_dir]

        all_cs_files = []
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".cs"):
                    all_cs_files.append(os.path.abspath(os.path.join(root, file)))

        test_paths, non_test_paths = self.split_test_and_non_test(all_cs_files, test_files)

        if not all_cs_files:
            logging.warning(f"No C# files found in {repo_dir}")
        else:
            logging.info(f"Total number of C# files found: {len(all_cs_files)}")

        test_dirs = list(set([os.path.dirname(path) for path in test_paths]))
        non_test_dirs = list(set([os.path.dirname(path) for path in non_test_paths]))

        filtered_non_test_dirs = []
        for non_test_dir in non_test_dirs:
            if not any(os.path.commonpath([non_test_dir, test_dir]) == test_dir for test_dir in test_dirs):
                filtered_non_test_dirs.append(non_test_dir)
            else:
                logging.info(f"Excluding non-test directory {non_test_dir} as it is within a test directory.")

        grouped_test_dirs = self.merge_single_child_directories(test_dirs, repo_dir)
        grouped_non_test_dirs = self.merge_single_child_directories(filtered_non_test_dirs, repo_dir)

        logging.info(f"Test directories: {grouped_test_dirs}")
        logging.info(f"Non-test directories: {grouped_non_test_dirs}")

        self.create_solution_and_projects(repo_dir, grouped_test_dirs, grouped_non_test_dirs)

    def process_all_repos(self):
        """Process all repos in cache_dir based on input_jsonl data."""
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(levelname)s:%(message)s')

        with open(self.input_jsonl, 'r') as f:
            instances = [json.loads(line) for line in f]

        for instance in instances:
            instance_id = instance['instance_id']
            repo_dir = os.path.join(self.cache_dir, instance_id)
            if os.path.exists(repo_dir):
                logging.info(f"Processing repo: {repo_dir}")
                self.process_repo(repo_dir, instance)
            else:
                logging.warning(f"Repo not found: {repo_dir}")