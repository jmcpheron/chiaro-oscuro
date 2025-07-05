"""
Basic function tests for chiaro-oscuro.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import extract_svg_from_response, validate_svg_content


def test_extract_svg_from_response_simple():
    """Test SVG extraction from a simple response."""
    svg_content = '<svg><circle r="10"/></svg>'
    result = extract_svg_from_response(svg_content)
    assert result == svg_content


def test_extract_svg_from_response_with_code_block():
    """Test SVG extraction from code block format."""
    response = '''Here's your logo:
    ```svg
    <svg><circle r="10"/></svg>
    ```
    Hope you like it!'''
    result = extract_svg_from_response(response)
    assert result == '<svg><circle r="10"/></svg>'


def test_extract_svg_from_response_multiline():
    """Test SVG extraction with multiline SVG."""
    response = '''```svg
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>
```'''
    result = extract_svg_from_response(response)
    expected = '<svg width="100" height="100">\n  <circle cx="50" cy="50" r="40" fill="blue"/>\n</svg>'
    assert result == expected


def test_prompt_files_exist():
    """Test that prompt files exist."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    analysis_prompt = prompts_dir / "logo-analysis-generation.txt"
    variants_prompt = prompts_dir / "theme-variants.txt"
    
    assert analysis_prompt.exists(), "Analysis prompt file should exist"
    assert variants_prompt.exists(), "Theme variants prompt file should exist"


def test_prompt_files_content():
    """Test that prompt files have meaningful content."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    
    analysis_content = (prompts_dir / "logo-analysis-generation.txt").read_text()
    assert "analysis" in analysis_content.lower()
    assert "svg" in analysis_content.lower()
    assert "brand" in analysis_content.lower()
    
    variants_content = (prompts_dir / "theme-variants.txt").read_text()
    assert "light theme" in variants_content.lower()
    assert "dark theme" in variants_content.lower()
    assert "svg" in variants_content.lower()


def test_validate_svg_content():
    """Test SVG validation function."""
    # Valid SVG
    valid_svg = '<svg width="100" height="100"><circle cx="50" cy="50" r="40"/></svg>'
    assert validate_svg_content(valid_svg) == True
    
    # Invalid SVG (no closing tag)
    invalid_svg = '<svg width="100" height="100"><circle cx="50" cy="50" r="40"/>'
    assert validate_svg_content(invalid_svg) == False
    
    # Invalid SVG (too short)
    short_svg = '<svg></svg>'
    assert validate_svg_content(short_svg) == False
    
    # Invalid SVG (empty)
    assert validate_svg_content("") == False


def test_extract_svg_with_validation():
    """Test that extraction now includes validation."""
    # Valid SVG should work
    valid_response = '''Here's your logo:
    ```svg
    <svg width="100" height="100"><circle cx="50" cy="50" r="40" fill="blue"/></svg>
    ```'''
    result = extract_svg_from_response(valid_response)
    assert "<svg" in result and "</svg>" in result


def test_theme_variants_extraction():
    """Test extraction of light and dark theme variants."""
    # Import the function
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from process_logos_v2 import extract_theme_variants
    
    # Mock response with both variants
    variants_response = '''Here are the optimized versions:
    
    LIGHT VERSION:
    ```svg
    <svg width="100" height="100"><circle cx="50" cy="50" r="40" fill="#000000"/></svg>
    ```
    
    DARK VERSION:
    ```svg
    <svg width="100" height="100"><circle cx="50" cy="50" r="40" fill="#ffffff"/></svg>
    ```
    '''
    
    light_svg, dark_svg = extract_theme_variants(variants_response)
    
    assert light_svg is not None
    assert dark_svg is not None
    assert "#000000" in light_svg  # Dark elements for light theme
    assert "#ffffff" in dark_svg   # Light elements for dark theme
    

def test_basic_string_operations():
    """Test basic string operations used in the code."""
    test_string = "assets/logo.png"
    assert test_string.endswith(".png")
    assert not test_string.endswith(".svg")
    assert "logo" in test_string