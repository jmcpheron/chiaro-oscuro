#!/usr/bin/env python3
"""
Test script to simulate how the action behaves in an external repository.
This helps diagnose why SVG files aren't being saved and branches aren't created.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import setup_logging, update_readme_with_picture_tag
from process_logos_llm import extract_theme_variants

logger = setup_logging()


def test_external_repo_simulation():
    """Simulate the action running in an external repository."""
    # Create a temporary directory to simulate external repo
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.info(f"🧪 Created temp directory to simulate external repo: {temp_dir}")
        
        # Set up environment as if running in GitHub Actions
        original_workspace = os.environ.get("GITHUB_WORKSPACE")
        os.environ["GITHUB_WORKSPACE"] = temp_dir
        
        # Create a simple README
        readme_path = Path(temp_dir) / "README.md"
        readme_path.write_text("# Test Project\n\nThis is a test project.\n")
        logger.info(f"📝 Created README at: {readme_path}")
        
        # Create output directory
        output_dir = Path(temp_dir) / "assets"
        output_dir.mkdir(exist_ok=True)
        logger.info(f"📁 Created output directory: {output_dir}")
        
        # Simulate LLM response with two SVG variants
        llm_response = """
Here are the logo variants for your project:

## Light Theme Logo
```svg
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>Test Logo (Light Theme)</title>
  <desc>Logo optimized for light backgrounds</desc>
  <rect width="200" height="200" fill="white" />
  <circle cx="100" cy="100" r="60" fill="#333" />
  <text x="100" y="110" font-family="Arial" font-size="24" fill="white" text-anchor="middle">TEST</text>
</svg>
```

## Dark Theme Logo
```svg
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>Test Logo (Dark Theme)</title>
  <desc>Logo optimized for dark backgrounds</desc>
  <rect width="200" height="200" fill="black" />
  <circle cx="100" cy="100" r="60" fill="#fff" />
  <text x="100" y="110" font-family="Arial" font-size="24" fill="black" text-anchor="middle">TEST</text>
</svg>
```
"""
        
        # Test extraction
        logger.info("🔍 Testing SVG extraction...")
        light_svg, dark_svg = extract_theme_variants(llm_response)
        
        if light_svg and dark_svg:
            logger.info("✅ Successfully extracted both theme variants")
            
            # Save SVGs
            light_path = output_dir / "logo-light.svg"
            dark_path = output_dir / "logo-dark.svg"
            
            light_path.write_text(light_svg)
            dark_path.write_text(dark_svg)
            
            logger.info(f"💾 Saved light logo to: {light_path}")
            logger.info(f"💾 Saved dark logo to: {dark_path}")
            
            # Test README update
            logger.info("📝 Testing README update...")
            try:
                update_readme_with_picture_tag(str(light_path), str(dark_path))
                
                # Check if README was updated
                updated_readme = readme_path.read_text()
                if "<picture>" in updated_readme:
                    logger.info("✅ README successfully updated with picture element")
                    logger.info(f"📄 Updated README preview:\n{updated_readme[:500]}...")
                else:
                    logger.error("❌ README was not updated with picture element")
                    
            except Exception as e:
                logger.error(f"❌ Failed to update README: {e}")
                
        else:
            logger.error("❌ Failed to extract SVG variants")
            
        # List all files created
        logger.info("\n📂 Files in simulated repo:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            logger.info(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                logger.info(f"{subindent}{file}")
                
        # Restore original environment
        if original_workspace:
            os.environ["GITHUB_WORKSPACE"] = original_workspace
        else:
            os.environ.pop("GITHUB_WORKSPACE", None)


if __name__ == "__main__":
    test_external_repo_simulation()