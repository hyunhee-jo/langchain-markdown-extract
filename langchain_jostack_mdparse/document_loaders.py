"""LangChain Document Loader for jostack-mdparse."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Iterator, List, Optional, Union

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from jostack_mdparse import extract as _extract

logger = logging.getLogger(__name__)


class MarkdownExtractLoader(BaseLoader):
    """Load Markdown files using jostack-mdparse and return LangChain Documents.

    This loader wraps the jostack-mdparse library to parse Markdown files
    and return structured content as LangChain Document objects.

    Example:
        .. code-block:: python

            from langchain_jostack_mdparse import MarkdownExtractLoader

            loader = MarkdownExtractLoader("README.md")
            docs = loader.load()
    """

    def __init__(
        self,
        file_path: Union[str, Path, List[Union[str, Path]]],
        # --- BEGIN SYNCED PARAMS ---
        format: str = "text",
        quiet: bool = False,
        heading_level: Optional[Union[str, List[str]]] = None,
        sections: Optional[Union[str, List[str]]] = None,
        include_frontmatter: bool = True,
        strip_html: bool = False,
        include_code_blocks: bool = True,
        include_toc: bool = False,
        flatten_lists: bool = False,
        section_separator: Optional[str] = None,
        normalize_links: bool = False,
        detect_tables: bool = False,
        # --- END SYNCED PARAMS ---
        split_sections: bool = True,
    ) -> None:
        """Initialize the loader.

        Args:
            file_path: Path to a Markdown file, directory, or list of paths.
            format: Output format from jostack-mdparse. Default: "text".
            quiet: Suppress console logging output.
            heading_level: Filter by heading levels (comma-separated).
            sections: Extract only sections matching heading text (comma-separated).
            include_frontmatter: Include YAML/TOML frontmatter in output.
            strip_html: Strip inline HTML tags from Markdown content.
            include_code_blocks: Include fenced code blocks in output.
            include_toc: Add a generated table of contents to the output.
            flatten_lists: Flatten nested lists into a single level.
            section_separator: Separator between sections in text output.
            normalize_links: Convert relative links to absolute.
            split_sections: Split output into per-section Documents. Default: True.
        """
        if isinstance(file_path, (str, Path)):
            self.file_paths = [Path(file_path)]
        else:
            self.file_paths = [Path(p) for p in file_path]

        # --- BEGIN SYNCED ASSIGNMENTS ---
        self.format = format
        self.quiet = quiet
        self.heading_level = heading_level
        self.sections = sections
        self.include_frontmatter = include_frontmatter
        self.strip_html = strip_html
        self.include_code_blocks = include_code_blocks
        self.include_toc = include_toc
        self.flatten_lists = flatten_lists
        self.section_separator = section_separator
        self.normalize_links = normalize_links
        self.detect_tables = detect_tables
        # --- END SYNCED ASSIGNMENTS ---

        self.split_sections = split_sections

    def lazy_load(self) -> Iterator[Document]:
        """Lazily load Documents from Markdown files.

        Yields:
            Document objects with extracted content and metadata.
        """
        for file_path in self.file_paths:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # --- BEGIN SYNCED CONVERT KWARGS ---
            convert_kwargs: dict[str, Any] = {
                "format": self.format,
                "heading_level": self.heading_level,
                "sections": self.sections,
                "include_frontmatter": self.include_frontmatter,
                "strip_html": self.strip_html,
                "include_code_blocks": self.include_code_blocks,
                "include_toc": self.include_toc,
                "flatten_lists": self.flatten_lists,
                "section_separator": self.section_separator,
                "normalize_links": self.normalize_links,
                "detect_tables": self.detect_tables,
            }
            # --- END SYNCED CONVERT KWARGS ---

            try:
                result = _extract(
                    file_path,
                    quiet=self.quiet,
                    **convert_kwargs,
                )
            except Exception:
                logger.exception("Failed to extract %s", file_path)
                raise

            source_name = str(file_path)

            if self.split_sections and self.format in ("json",):
                yield from self._split_json_into_sections(result, source_name)
            elif self.split_sections and self.format in ("text", "html"):
                yield from self._split_text_into_sections(result, source_name)
            else:
                yield Document(
                    page_content=result,
                    metadata={"source": source_name, "format": self.format},
                )

    def _split_json_into_sections(
        self,
        content: str,
        source_name: str,
    ) -> Iterator[Document]:
        """Split JSON output into per-section Documents."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            yield Document(
                page_content=content,
                metadata={"source": source_name, "format": self.format},
            )
            return

        sections = data.get("sections", [])
        if not sections:
            yield Document(
                page_content=content,
                metadata={"source": source_name, "format": self.format},
            )
            return

        for i, section in enumerate(sections):
            title = section.get("title", "")
            section_content = section.get("content", "")
            if title:
                page_content = (
                    f"# {title}\n\n{section_content}" if section_content else f"# {title}"
                )
            else:
                page_content = section_content

            yield Document(
                page_content=page_content,
                metadata={
                    "source": source_name,
                    "format": self.format,
                    "section": i,
                    "section_title": title,
                    "heading_level": section.get("level", 0),
                },
            )

    def _split_text_into_sections(
        self,
        content: str,
        source_name: str,
    ) -> Iterator[Document]:
        """Split text/html output into per-section Documents using heading markers."""
        import re

        parts = re.split(r"(?=^#{1,6}\s)", content, flags=re.MULTILINE)

        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue

            heading_match = re.match(r"^(#{1,6})\s+(.+?)$", part, re.MULTILINE)
            title = heading_match.group(2) if heading_match else ""
            level = len(heading_match.group(1)) if heading_match else 0

            yield Document(
                page_content=part,
                metadata={
                    "source": source_name,
                    "format": self.format,
                    "section": i,
                    "section_title": title,
                    "heading_level": level,
                },
            )
