# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

chiaro-oscuro is a GitHub Action that generates SVG logos from scratch using AI. It creates two theme-aware variants (light and dark) using GitHub's built-in models system. **Important: This project does NOT analyze existing images - it creates new logos based on project descriptions.**

## Development Commands

**Package Manager**: UV (modern Python package manager)

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest
uv run pytest --cov=src --cov-report=html  # with coverage

# Linting and formatting
uv run black src tests
uv run isort src tests
uv run flake8 src tests
uv run mypy src

# Run the main script locally
uv run python -m src.process_logos_llm
```

## Architecture Overview

### Single-Step Logo Generation

The project uses a simplified single-step approach:

1. **GitHub Action** (`action.yml`)
   - Accepts project name, description, and style inputs
   - Uses LLM CLI with GitHub Models (no external API keys needed)
   - Generates logos in one AI call

2. **Python Processing** (`src/`)
   - `process_logos_llm.py`: Extracts SVG variants from AI response
   - `utils.py`: SVG validation and README update functions

3. **AI Prompt** (`prompts/generate-logo.txt`)
   - Template for generating both light/dark variants in one request
   - Placeholders for project name, description, and style

### Key Technical Details

- **Authentication**: Uses GitHub token as `GITHUB_MODELS_KEY` environment variable
- **Models**: Supports github/gpt-4o-mini, github/llama-3.1-70b-instruct, github/deepseek-r1
- **No Image Analysis**: This tool creates logos from scratch, it does not analyze existing images
- **Git Integration**: Creates pull requests with generated logos

### GitHub Action Workflow

1. User provides project name, description, and style preference
2. Action generates prompt from template
3. LLM CLI creates two SVG variants via GitHub Models
4. Python script extracts and saves both variants
5. Updates README.md with `<picture>` element
6. Creates PR with changes

Required permissions: `contents: write`, `pull-requests: write`, `models: read`