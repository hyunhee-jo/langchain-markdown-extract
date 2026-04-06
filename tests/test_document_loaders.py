"""Unit tests for MarkdownExtractLoader."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from langchain_md_extract import MarkdownExtractLoader


class TestMarkdownExtractLoaderInit:
    """Tests for loader initialization."""

    def test_single_file_path(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(md)
        assert len(loader.file_paths) == 1

    def test_string_path(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(str(md))
        assert len(loader.file_paths) == 1

    def test_multiple_paths(self, tmp_path: Path) -> None:
        md1 = tmp_path / "a.md"
        md2 = tmp_path / "b.md"
        md1.write_text("# A", encoding="utf-8")
        md2.write_text("# B", encoding="utf-8")
        loader = MarkdownExtractLoader([md1, md2])
        assert len(loader.file_paths) == 2

    def test_default_params(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(md)
        assert loader.format == "text"
        assert loader.quiet is False
        assert loader.heading_level is None
        assert loader.sections is None
        assert loader.include_frontmatter is True
        assert loader.strip_html is False
        assert loader.include_code_blocks is True
        assert loader.include_toc is False
        assert loader.flatten_lists is False
        assert loader.section_separator is None
        assert loader.normalize_links is False
        assert loader.split_sections is True

    def test_custom_params(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(
            md,
            format="json",
            quiet=True,
            heading_level="1,2",
            sections="Intro",
            include_frontmatter=False,
            strip_html=True,
            include_code_blocks=False,
            include_toc=True,
            flatten_lists=True,
            section_separator="---",
            normalize_links=True,
            split_sections=False,
        )
        assert loader.format == "json"
        assert loader.quiet is True
        assert loader.heading_level == "1,2"
        assert loader.sections == "Intro"
        assert loader.include_frontmatter is False
        assert loader.strip_html is True
        assert loader.include_code_blocks is False
        assert loader.include_toc is True
        assert loader.flatten_lists is True
        assert loader.section_separator == "---"
        assert loader.normalize_links is True
        assert loader.split_sections is False


class TestMarkdownExtractLoaderLoad:
    """Tests for loader document loading."""

    def test_load_returns_documents(self, mock_extract: MagicMock, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(md, format="json")
        docs = loader.load()
        assert len(docs) == 1
        assert docs[0].metadata["source"] == str(md)

    def test_load_json_split_sections(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")

        mock_result = json.dumps(
            {
                "source": str(md),
                "sections": [
                    {"level": 1, "title": "Intro", "content": "Hello"},
                    {"level": 2, "title": "Details", "content": "World"},
                ],
            }
        )

        with patch(
            "langchain_md_extract.document_loaders._extract", return_value=mock_result
        ):
            loader = MarkdownExtractLoader(md, format="json")
            docs = loader.load()

        assert len(docs) == 2
        assert docs[0].metadata["section_title"] == "Intro"
        assert docs[0].metadata["heading_level"] == 1
        assert docs[1].metadata["section_title"] == "Details"
        assert docs[1].metadata["heading_level"] == 2
        assert "# Intro" in docs[0].page_content

    def test_load_text_split_sections(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")

        mock_result = "# Intro\n\nHello world.\n\n## Details\n\nSome details."

        with patch(
            "langchain_md_extract.document_loaders._extract", return_value=mock_result
        ):
            loader = MarkdownExtractLoader(md, format="text")
            docs = loader.load()

        assert len(docs) >= 2
        titles = [d.metadata["section_title"] for d in docs]
        assert "Intro" in titles
        assert "Details" in titles

    def test_load_no_split(self, mock_extract: MagicMock, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(md, format="text", split_sections=False)
        docs = loader.load()
        assert len(docs) == 1

    def test_file_not_found(self, tmp_path: Path) -> None:
        loader = MarkdownExtractLoader(tmp_path / "nonexistent.md")
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_extract_kwargs_passed(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")

        with patch("langchain_md_extract.document_loaders._extract") as mock:
            mock.return_value = "# Test\n\nContent"
            loader = MarkdownExtractLoader(
                md,
                format="text",
                heading_level="1",
                strip_html=True,
                quiet=True,
            )
            loader.load()

            mock.assert_called_once()
            call_kwargs = mock.call_args
            assert call_kwargs.kwargs["heading_level"] == "1"
            assert call_kwargs.kwargs["strip_html"] is True
            assert call_kwargs.kwargs["quiet"] is True

    def test_multiple_files(self, tmp_path: Path) -> None:
        md1 = tmp_path / "a.md"
        md2 = tmp_path / "b.md"
        md1.write_text("# A\n\nContent A", encoding="utf-8")
        md2.write_text("# B\n\nContent B", encoding="utf-8")

        mock_results = iter(
            [
                '{"source": "a.md", "sections": '
                '[{"level": 1, "title": "A", "content": "Content A"}]}',
                '{"source": "b.md", "sections": '
                '[{"level": 1, "title": "B", "content": "Content B"}]}',
            ]
        )

        with patch(
            "langchain_md_extract.document_loaders._extract",
            side_effect=lambda *a, **kw: next(mock_results),
        ):
            loader = MarkdownExtractLoader([md1, md2], format="json")
            docs = loader.load()

        assert len(docs) == 2

    def test_lazy_load_is_iterator(self, mock_extract: MagicMock, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")
        loader = MarkdownExtractLoader(md, format="json")
        result = loader.lazy_load()
        assert hasattr(result, "__next__")

    def test_extract_error_raises(self, tmp_path: Path) -> None:
        md = tmp_path / "test.md"
        md.write_text("# Test", encoding="utf-8")

        with patch(
            "langchain_md_extract.document_loaders._extract",
            side_effect=RuntimeError("parse error"),
        ):
            loader = MarkdownExtractLoader(md)
            with pytest.raises(RuntimeError, match="parse error"):
                loader.load()
