# CLAUDE.md

## Project Overview

langchain-md-extract is a LangChain Document Loader that wraps md-extract.

## Architecture

- `langchain_md_extract/document_loaders.py` — Core loader (BaseLoader subclass)
- 3 SYNCED marker blocks: PARAMS, ASSIGNMENTS, CONVERT KWARGS
- Parameters are auto-generated from upstream md-extract's options.json

## Key Design Decisions

- **SYNCED markers**: Code between markers is auto-generated, do not edit manually
- **split_sections**: Loader-specific param, outside SYNCED markers
- **format default "text"**: Overrides upstream "json" for RAG use case
- **Version 0.0.0**: Injected at build time via sed in release.yml

## Commands

```bash
make test     # pytest + pytest-socket
make lint     # ruff check + format
```

## Conventions

- Commits: conventional commit format (English)
- PRs: single purpose, <10 files, <500 lines
