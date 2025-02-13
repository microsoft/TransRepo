import os
import argparse
from pom_manager import create_default_pom, setup_jacoco
from directory_setup import create_directory_structure
from test_runner import run_tests
from report_parser import parse_coverage_report

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Run JaCoCo coverage analysis on a Java Maven project')
    parser.add_argument('--repo_path', '-p', type=str, required=True,
                       help='Path to the Java Maven project')
    args = parser.parse_args()
    
    # Get and validate project path
    project_path = os.path.abspath(args.repo_path)
    if not os.path.exists(project_path):
        print(f"Error: Repository path does not exist: {project_path}")
        return
    
    pom_path = os.path.join(project_path, 'pom.xml')
    
    # Check and create project structure
    create_directory_structure(project_path)
    
    # Check if pom.xml exists, create if not
    if not os.path.exists(pom_path):
        print("pom.xml not found, creating default pom.xml...")
        if not create_default_pom(project_path):
            print("Failed to create pom.xml")
            return
        print("Created default pom.xml")
    
    print("1. Configuring JaCoCo plugin...")
    if not setup_jacoco(pom_path):
        print("Failed to configure JaCoCo")
        return
    
    print("2. Running tests...")
    if not run_tests(project_path):
        print("Test execution failed")
        return
    
    print("3. Parsing coverage report...")
    if not parse_coverage_report(project_path):
        print("Failed to parse coverage report")
        return

if __name__ == "__main__":
    main()