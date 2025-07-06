"""
Utility functions for chiaro-oscuro logo generation.
"""

import logging
import os
import re
from pathlib import Path


def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


def validate_svg_content(svg_content: str) -> bool:
    """Validate that SVG content is well-formed."""
    try:
        # Basic structural checks
        if not svg_content.strip():
            return False
        if not svg_content.strip().startswith("<svg"):
            return False
        if not svg_content.strip().endswith("</svg>"):
            return False

        # Check for balanced tags (basic validation)
        if svg_content.count("<svg") != svg_content.count("</svg>"):
            return False

        # Minimum length check (avoid empty SVGs)
        if len(svg_content.strip()) < 20:
            return False

        return True
    except Exception:
        return False


def extract_svg_from_response(response_text: str) -> str:
    """Extract SVG content from AI response with validation."""
    # Look for SVG content between ```svg and ``` or <svg> tags
    svg_patterns = [
        r"```svg\s*(.*?)\s*```",
        r"```\s*(.*?<svg.*?</svg>.*?)\s*```",
        r"(<svg[^>]*>.*?</svg>)",
    ]

    candidates = []

    for pattern in svg_patterns:
        match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if match:
            svg_content = match.group(1).strip()
            if validate_svg_content(svg_content):
                candidates.append(svg_content)

    # If no pattern matches, check if the entire response is SVG
    if response_text.strip().startswith("<svg") and response_text.strip().endswith("</svg>"):
        if validate_svg_content(response_text.strip()):
            candidates.append(response_text.strip())

    if not candidates:
        raise ValueError(
            f"No valid SVG content found in AI response. "
            f"Response length: {len(response_text)} chars, "
            f"starts with: {response_text[:100]}"
        )

    # Return the longest valid SVG (likely the most complete)
    return max(candidates, key=len)


def update_readme_with_picture_tag(light_logo_path: str, dark_logo_path: str) -> None:
    """Update README.md with GitHub's picture element for theme-aware logos."""
    logger = logging.getLogger(__name__)
    # Use GITHUB_WORKSPACE if available, otherwise current directory
    workspace = os.environ.get("GITHUB_WORKSPACE", ".")
    readme_path = Path(workspace) / "README.md"

    if not readme_path.exists():
        logger.info("Creating new README.md")
        readme_content = ""
    else:
        logger.info("Updating existing README.md")
        readme_content = readme_path.read_text()

    # Convert paths to be relative to the workspace
    workspace_path = Path(workspace)
    light_path = Path(light_logo_path)
    dark_path = Path(dark_logo_path)

    # Make paths relative if they're under the workspace
    try:
        light_rel = light_path.relative_to(workspace_path)
        dark_rel = dark_path.relative_to(workspace_path)
    except ValueError:
        # If paths are not relative to workspace, use as-is
        light_rel = light_path
        dark_rel = dark_path

    # Create the picture element with relative paths
    picture_element = f"""<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{dark_rel.as_posix()}">
    <source media="(prefers-color-scheme: light)" srcset="{light_rel.as_posix()}">
    <img src="{light_rel.as_posix()}" alt="Project logo" width="200">
  </picture>
</p>"""

    # Check if README already has a picture element
    if "<picture>" in readme_content:
        # Replace existing picture element
        pattern = r"<p[^>]*>\s*<picture>.*?</picture>\s*</p>"
        readme_content = re.sub(pattern, picture_element, readme_content, flags=re.DOTALL)
        logger.info("Replaced existing picture element")
    else:
        # Add picture element at the beginning
        if readme_content.startswith("#"):
            # Insert after the first heading
            lines = readme_content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("#") and i + 1 < len(lines):
                    lines.insert(i + 1, "\n" + picture_element + "\n")
                    break
            readme_content = "\n".join(lines)
        else:
            # Add at the very beginning
            readme_content = picture_element + "\n\n" + readme_content
        logger.info("Added new picture element")

    # Write updated content
    readme_path.write_text(readme_content)
    logger.info("✅ README.md updated with theme-aware logos")
