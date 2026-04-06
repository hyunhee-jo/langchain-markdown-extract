"""Shared test fixtures for langchain-md-extract."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def sample_md(tmp_path: Path) -> Path:
    """Create a sample Markdown file for testing."""
    md_file = tmp_path / "sample.md"
    md_file.write_text(
        "---\ntitle: Test\n---\n\n# Intro\n\nHello world.\n\n## Details\n\nSome details here.\n",
        encoding="utf-8",
    )
    return md_file


@pytest.fixture
def mock_extract():
    """Mock md_extract.extract to avoid real dependency."""
    with patch("langchain_md_extract.document_loaders._extract") as mock:
        mock.return_value = (
            '{"source": "test.md", "sections": '
            '[{"level": 1, "title": "Intro", "content": "Hello"}]}'
        )
        yield mock
