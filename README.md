# TransRepo 🚀

TransRepo is a repository-level code translation benchmark focused on Java-to-C# translation, providing skeleton code and test cases for evaluation.

## Overview 📋

TransRepo presents a novel approach to repository-level code translation evaluation:
- 🎯 Generates C# skeleton code from Java repositories
- 🧪 Translates Java test files to C# test files
- 📊 Provides evaluation metrics for translated implementations
- 🔍 Focuses on preserving project structure and maintainability

## Dataset 📦

The benchmark dataset is available at "/data", containing:
- Original Java source files
- Translated C# skeleton code
- Translated C# test files
- Project configuration files (*.csproj)

## Usage 💻

### Language Versions
- Java 21 or later
- C# 12.0 (.NET 8.0) or later

### Python Dependencies
- Python 3.x
- tree-sitter >= 0.20.1
- tqdm >= 4.65.0

### Evaluation Command
```bash
python transrepo/verify/translated_code_validator.py \
    --skeleton-path /path/to/skeleton \
    --translated-path /path/to/translated \
    --json-path /path/to/json \
    --output-path /path/to/output \
    --progress-bar-length 50
```

### Baseline Translation and Evaluation
```bash
python transrepo/baseline/optimize_translation_without_skeleton.py \
    --input-path /path/to/java/source \
    --skeleton-path /path/to/csharp/skeleton \
    --output-path /path/to/output \
    --test-config /path/to/test/config
```
