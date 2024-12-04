# Preprocess: Java Repository Test Coverage Processor

A Python toolkit for automating JaCoCo test coverage analysis on Java Maven projects. This component helps prepare Java repositories for coverage analysis by handling Maven configuration, test execution, and coverage report generation.

## Usage
```bash
python3 main.py --repo_path /path/to/java/project
```

### Example
```bash
python main.py --repo_path ~/projects/my-java-app

Output:
1. Configuring JaCoCo plugin...
2. Running tests...
3. Parsing coverage report...

Coverage Report Summary:
================================================================================
Element                    Instructions  Branches     Lines        Methods      Classes      
--------------------------------------------------------------------------------
com.example               70.2%         65.8%        68.9%        75.0%        100%
================================================================================
```