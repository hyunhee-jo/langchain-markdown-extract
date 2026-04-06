.PHONY: test lint format build clean

test:
	pytest tests/ -v --disable-socket --allow-unix-socket

lint:
	ruff check langchain_markdown_extract/ tests/
	ruff format --check langchain_markdown_extract/ tests/

format:
	ruff check --fix langchain_markdown_extract/ tests/
	ruff format langchain_markdown_extract/ tests/

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
