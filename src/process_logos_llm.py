#!/usr/bin/env python3
"""
Process AI-generated logo responses using LLM CLI framework.
Implements single-step logo generation with light/dark theme variants.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

from utils import (
    setup_logging,
    update_readme_with_picture_tag,
    validate_svg_content,
)

logger = setup_logging()


def extract_theme_variants(logo_response: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract light and dark theme variants from the LLM logo response."""
    light_svg = None
    dark_svg = None

    logger.info(f"🔍 Extracting theme variants from {len(logo_response)} character LLM response")

    # Save full response for debugging
    try:
        with open("debug_logo_response.txt", "w", encoding="utf-8") as f:
            f.write(f"LLM LOGO RESPONSE DEBUG:\n\n{logo_response}")
        logger.info("💾 Saved full LLM response to debug_logo_response.txt")
    except Exception as e:
        logger.warning(f"Could not save debug response: {e}")

    # Extract all SVG blocks using multiple patterns
    all_svgs = []

    # Try code block pattern first
    svg_pattern = r"```(?:svg)?\s*(.*?)\s*```"
    code_blocks = re.findall(svg_pattern, logo_response, re.DOTALL | re.IGNORECASE)

    for block in code_blocks:
        if "<svg" in block and "</svg>" in block:
            all_svgs.append(block)

    # If no code blocks, try direct SVG tags
    if not all_svgs:
        svg_direct_pattern = r"(<svg[^>]*>.*?</svg>)"
        direct_svgs = re.findall(svg_direct_pattern, logo_response, re.DOTALL | re.IGNORECASE)
        all_svgs.extend(direct_svgs)

    logger.info(f"🔍 Found {len(all_svgs)} SVG blocks in LLM response")

    # Validate each SVG
    valid_svgs = []
    for i, svg_content in enumerate(all_svgs):
        svg_clean = svg_content.strip()
        if validate_svg_content(svg_clean):
            valid_svgs.append(svg_clean)
            logger.info(f"✅ SVG block {i+1} is valid ({len(svg_clean)} chars)")

            # Check for theme indicators in comments or descriptions
            if "light" in svg_clean.lower() and not light_svg:
                light_svg = svg_clean
                logger.info("   → Identified as LIGHT theme variant")
            elif "dark" in svg_clean.lower() and not dark_svg:
                dark_svg = svg_clean
                logger.info("   → Identified as DARK theme variant")
        else:
            logger.warning(f"❌ SVG block {i+1} failed validation")
            logger.debug(f"   Preview: {svg_clean[:100]}...")

    logger.info(f"🎯 Total valid SVGs: {len(valid_svgs)}")

    # If theme detection didn't work, use positional assignment
    if not light_svg and not dark_svg and len(valid_svgs) >= 2:
        light_svg = valid_svgs[0]
        dark_svg = valid_svgs[1]
        logger.info("✅ Using positional assignment: first=light, second=dark")
    elif not light_svg and not dark_svg and len(valid_svgs) == 1:
        logger.error("❌ Only one SVG found when two were expected")
        return None, None

    # Final validation
    logger.info("🎯 FINAL EXTRACTION RESULTS:")
    logger.info(f"   Light SVG: {'✅ Found' if light_svg else '❌ Missing'}")
    logger.info(f"   Dark SVG: {'✅ Found' if dark_svg else '❌ Missing'}")

    if not light_svg or not dark_svg:
        logger.error("❌ Failed to extract both theme variants")
        return None, None

    return light_svg, dark_svg


def main():
    """Main execution function for single-step logo generation."""
    try:
        # Get configuration from environment variables
        output_dir = os.getenv("OUTPUT_DIR", "assets")
        logo_response_file = os.getenv("LOGO_RESPONSE_FILE")

        if not logo_response_file or not os.path.exists(logo_response_file):
            logger.error("❌ Logo response file not found")
            sys.exit(1)

        # Read LLM response
        with open(logo_response_file, "r", encoding="utf-8") as f:
            logo_response = f.read()

        logger.info("🤖 Processing LLM-generated logo response")
        logger.info(f"📂 Output directory: {output_dir}")
        logger.info(f"📊 Response size: {len(logo_response)} characters")

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Extract theme variants
        logger.info("🔍 Extracting light and dark theme variants...")
        light_svg, dark_svg = extract_theme_variants(logo_response)

        if not light_svg or not dark_svg:
            logger.error("❌ Failed to extract both theme variants from LLM response")
            sys.exit(1)

        # Save logos
        light_path = Path(output_dir) / "logo-light.svg"
        dark_path = Path(output_dir) / "logo-dark.svg"

        with open(light_path, "w", encoding="utf-8") as f:
            f.write(light_svg)
        logger.info(f"✅ Saved light theme logo to: {light_path}")

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(dark_svg)
        logger.info(f"✅ Saved dark theme logo to: {dark_path}")

        # Update README with theme-aware logos
        logger.info("🎉 Updating README with theme-aware logos")
        update_readme_with_picture_tag(str(light_path), str(dark_path))

        # Set outputs for GitHub Actions
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"light-logo-path={light_path}\n")
                f.write(f"dark-logo-path={dark_path}\n")

        logger.info("🎉 Successfully generated theme-aware logos using GitHub Models")

    except Exception as e:
        logger.error(f"❌ Logo processing failed: {str(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
