<!-- AI-AGENT-SUMMARY
name: langchain-jostack-mdparse
category: LangChain document loader, Markdown extraction for RAG
license: Apache-2.0
solves: [Load Markdown files as LangChain Document objects, section-level splitting]
input: Markdown files (.md)
output: LangChain Document objects (text, JSON, HTML)
sdk: Python
requirements: Python 3.10+
key-differentiators: [LangChain-native BaseLoader, per-section splitting, auto-synced from upstream]
-->

# langchain-jostack-mdparse

[![CI](https://github.com/hyunhee-jo/langchain-jostack-mdparse/actions/workflows/ci.yml/badge.svg)](https://github.com/hyunhee-jo/langchain-jostack-mdparse/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A LangChain Document Loader for [jostack-mdparse](https://github.com/hyunhee-jo/jostack-mdparse).

## Installation

```bash
pip install langchain-jostack-mdparse
```

## Quick Start

```python
from langchain_jostack_mdparse import MarkdownExtractLoader

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
| `format` | `str` | `"text"` | Output format. Values: json, text, html. Default: json |
| `quiet` | `bool` | `False` | Suppress console logging output |
| `heading_level` | `str` | `None` | Filter by heading levels (comma-separated, e.g. '1,2,3'). Default: all levels |
| `sections` | `str` | `None` | Extract only sections matching the given heading text (comma-separated). Case-insensitive substring match |
| `include_frontmatter` | `bool` | `True` | Include YAML/TOML frontmatter in output. Default: true |
| `strip_html` | `bool` | `False` | Strip inline HTML tags from Markdown content |
| `include_code_blocks` | `bool` | `True` | Include fenced code blocks in output. Default: true |
| `include_toc` | `bool` | `False` | Add a generated table of contents to the output |
| `flatten_lists` | `bool` | `False` | Flatten nested lists into a single level |
| `section_separator` | `str` | `None` | Separator between sections in text output. Use %section-title% for heading text. Default: none |
| `normalize_links` | `bool` | `False` | Convert relative links to absolute using the source file path |
| `detect_tables` | `bool` | `False` | Detect and extract Markdown tables as structured data |
<!-- END SYNCED PARAMS TABLE -->

## Development

```bash
pip install -e .
make test
make lint
```

## License

[Apache-2.0](LICENSE)
