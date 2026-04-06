<!-- AI-AGENT-SUMMARY
name: langchain-markdown-extract
category: LangChain document loader, Markdown extraction for RAG
license: Apache-2.0
solves: [Load Markdown files as LangChain Document objects, section-level splitting]
input: Markdown files (.md)
output: LangChain Document objects (text, JSON, HTML)
sdk: Python
requirements: Python 3.10+
key-differentiators: [LangChain-native BaseLoader, per-section splitting, auto-synced from upstream]
-->

# langchain-markdown-extract

[![CI](https://github.com/hyunhee-jo/langchain-markdown-extract/actions/workflows/ci.yml/badge.svg)](https://github.com/hyunhee-jo/langchain-markdown-extract/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A LangChain Document Loader for [markdown-extract](https://github.com/hyunhee-jo/markdown-extract).

## Installation

```bash
pip install langchain-markdown-extract
```

## Quick Start

```python
from langchain_markdown_extract import MarkdownExtractLoader

# Load a single file
loader = MarkdownExtractLoader("README.md")
docs = loader.load()

# Load with options
loader = MarkdownExtractLoader(
    "docs/guide.md",
    heading_level="1,2",
    strip_html=True,
    split_sections=True,
)
docs = loader.load()

# Load multiple files
loader = MarkdownExtractLoader(["a.md", "b.md"])
docs = loader.load()
```

## Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | `str \| Path \| List` | — | (Required) Path to Markdown file(s) |
| `split_sections` | `bool` | `True` | Split output into per-section Documents |
<!-- BEGIN SYNCED PARAMS TABLE -->
| `format` | `str` | `"text"` | Output format: json, text, html |
| `quiet` | `bool` | `False` | Suppress console logging |
| `heading_level` | `str` | `None` | Filter by heading levels (comma-separated) |
| `sections` | `str` | `None` | Extract sections by heading text (comma-separated) |
| `include_frontmatter` | `bool` | `True` | Include YAML/TOML frontmatter |
| `strip_html` | `bool` | `False` | Strip inline HTML tags |
| `include_code_blocks` | `bool` | `True` | Include fenced code blocks |
| `include_toc` | `bool` | `False` | Add generated table of contents |
| `flatten_lists` | `bool` | `False` | Flatten nested lists |
| `section_separator` | `str` | `None` | Separator between sections |
| `normalize_links` | `bool` | `False` | Convert relative links to absolute |
<!-- END SYNCED PARAMS TABLE -->

## Development

```bash
pip install -e .
make test
make lint
```

## License

[Apache-2.0](LICENSE)
