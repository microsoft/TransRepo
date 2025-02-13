# TransRepo 🚀

TransRepo is a repository-level code translation benchmark focused on Java-to-C# translation, providing skeleton code and test cases for evaluation.

## Overview 📋

TransRepo presents a novel approach to repository-level code translation evaluation:
- 🎯 Generates C# skeleton code from Java repositories
- 🧪 Translates Java test files to C# test files
- 📊 Provides evaluation metrics for translated implementations
- 🔍 Focuses on preserving project structure and maintainability

## Dataset 📦

The benchmark dataset is available at [TransRepo-Data](https://github.com/microsoft/TransRepo-Data), containing:
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
## Paper and Citation
[Skeleton-Guided-Translation: A Benchmarking Framework for Code Repository Translation with Fine-Grained Quality Evaluation](https://arxiv.org/abs/2501.16050) (Zhang et al., ARXIV 2025)

```
@inproceedings{zhang-etal-2025-skeleton,
    title = "Skeleton-Guided-Translation: A Benchmarking Framework for Code Repository Translation with Fine-Grained Quality Evaluation",
    author = "Zhang, Xing  and
      Wen, Jiaheng  and
      Yang, Fangkai  and
      Zhao, Pu  and
      Kang, Yu  and
      Wang, Junhao  and
      Wang, Maoquan  and
      Huang, Yufan  and
      Nallipogu, Elsie  and
      Lin, Qingwei  and
      Dang, Yingnong  and
      Rajmohan, Saravan  and
      Zhang, Dongmei  and
      Zhang, Qi",
    booktitle = "arXiv preprint",
    month = jan,
    year = "2025",
    publisher = "arXiv",
    url = "https://arxiv.org/abs/2501.16050",
    doi = "10.48550/arXiv.2501.16050",
    abstract = "The advancement of large language models has intensified the need to modernize enterprise applications and migrate legacy systems to secure, versatile languages."
}
```

## Trademarks 
This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
