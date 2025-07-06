# Chiaroscuro 🌓
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.svg">
    <img src="assets/logo-light.svg" alt="Project logo" width="200">
  </picture>
</p>

>From the workshops of Florence to the workflows of GitHub: `chiaro-oscuro` translates the timeless language of contrast into the living vocabulary of adaptive interfaces.


**Continuous AI-powered SVG generation with automatic theme variants**

[![CI](https://github.com/jmcpheron/chiaro-oscuro/actions/workflows/ci.yml/badge.svg)](https://github.com/jmcpheron/chiaro-oscuro/actions/workflows/ci.yml)
[![Powered by Continuous AI](https://img.shields.io/badge/Powered%20by-Continuous%20AI-blue)](https://githubnext.com/projects/continuous-ai/)
[![GitHub Models](https://img.shields.io/badge/Uses-GitHub%20Models-green)](https://github.com/marketplace/models)

## 🎯 What It Does

**chiaro-oscuro** demonstrates Continuous AI for automated asset generation. It uses LLMs to generate theme-aware SVG logos from text descriptions, ensuring technical compatibility with modern UI systems and accessibility standards.

<div align="center">
<table>
<tr>
<th>Light Theme</th>
<th>Dark Theme</th>
</tr>
<tr>
<td align="center"><img src="assets/logo-light.svg" alt="Light theme logo" width="120"></td>
<td align="center"><img src="assets/logo-dark.svg" alt="Dark theme logo" width="120"></td>
</tr>
<tr>
<td align="center"><b>Perfect for light backgrounds</b></td>
<td align="center"><b>Perfect for dark backgrounds</b></td>
</tr>
<tr>
<td align="center">High contrast, dark elements</td>
<td align="center">High contrast, light elements</td>
</tr>
</table>
</div>

### Technical Capabilities
- **Automated SVG Generation**: Creates vector graphics from text descriptions using LLMs
- **Theme-Aware Output**: Generates separate variants for `prefers-color-scheme: light/dark`
- **Accessibility Compliance**: Ensures WCAG 2.1 AA contrast ratios
- **Zero Dependencies**: Uses only GitHub's built-in infrastructure (Actions + Models)

## 🚀 Getting Started

Add AI-powered logo generation to your repository in minutes!

### Prerequisites
- A GitHub repository where you want a logo
- Actions enabled in your repository
- That's it! No API keys or external accounts needed

### Step 1: Create the Workflow
Create a new file `.github/workflows/generate-logo.yml` in your repository with this content:

```yaml
name: Generate Logo
on:
  workflow_dispatch:
    inputs:
      description:
        description: 'What does your project do?'
        required: true
        type: string

permissions:
  contents: write
  pull-requests: write
  models: read  # Required for GitHub's AI models

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate logo with AI
        uses: jmcpheron/chiaro-oscuro@v1
        with:
          project-name: ${{ github.event.repository.name }}
          description: ${{ inputs.description }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Step 2: Configure Your Repository
Enable GitHub Actions to create pull requests:
1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, check "Allow GitHub Actions to create and approve pull requests"
3. Save your changes

### Step 3: Generate Your Logo
1. Go to the **Actions** tab in your repository
2. Select **"Generate Logo"** from the workflow list
3. Click **"Run workflow"**
4. Enter a description of what your project does (e.g., "A Python library for data visualization")
5. Click the green **"Run workflow"** button

### Step 4: Review and Merge
After ~30 seconds:
- A pull request will appear with your new logos
- Review `assets/logo-light.svg` and `assets/logo-dark.svg`
- The PR will also update your README.md with theme-aware display
- Merge when you're happy with the results!

### 🎨 Customization Options

```yaml
- uses: jmcpheron/chiaro-oscuro@v1
  with:
    project-name: 'My Cool Project'  # Override repo name
    description: ${{ inputs.description }}
    style: 'minimal'  # Options: modern, minimal, playful, corporate, tech
    output-dir: 'images'  # Default: assets
    model: 'github/gpt-4o'  # Use a different AI model
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 📝 Example Results
Your README will automatically be updated with:
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.svg">
  <img src="assets/logo-light.svg" alt="Project logo" width="200">
</picture>
```

This ensures your logo looks great in both light and dark themes!

## ❓ Troubleshooting & FAQ

### Common Issues

**"GitHub Actions is not permitted to create or approve pull requests"**
- You need to enable this in Settings → Actions → General → Workflow permissions
- This is a one-time setup per repository

**"Models permission required"**
- Make sure your workflow includes `models: read` in the permissions section
- This allows the action to use GitHub's AI models

**"No pull request created"**
- Check the Actions tab for any error messages
- Ensure your default branch is named `main` (or update the workflow)
- Verify you have write permissions to the repository

### FAQ

**Q: Do I need any API keys?**
A: No! This uses GitHub's built-in AI models. Your GitHub token is all you need.

**Q: Can I regenerate if I don't like the logo?**
A: Yes! Just run the workflow again. Each run generates unique designs.

**Q: Where are the logos saved?**
A: By default in `assets/` directory. You can change this with the `output-dir` parameter.

**Q: Can I use this in a private repository?**
A: Yes, as long as your GitHub plan includes access to GitHub Models.

**Q: What if I already have a logo?**
A: The action will create new ones. Back up existing logos first if needed.

## 🔧 Continuous AI Implementation

This project exemplifies [Continuous AI](https://githubnext.com/projects/continuous-ai/) principles by automating repetitive technical tasks in software development:

### Continuous AI Characteristics
✅ **Automatable**: LLM-powered SVG generation with high reliability  
✅ **Event-Triggered**: Activated by workflow dispatch or repository events  
✅ **Integrated**: Native GitHub Actions + GitHub Models integration  
✅ **Auditable**: Full git history of generated assets and parameters  
✅ **Collaborative**: PR-based review workflow for generated content  


## 🚀 Quick Start

```yaml
# .github/workflows/generate-logo.yml
name: Generate Logo via Continuous AI
on:
  workflow_dispatch:
    inputs:
      project_name:
        description: 'Project identifier'
        required: true
      description:
        description: 'Technical description'
        required: true

permissions:
  contents: write
  pull-requests: write
  models: read

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jmcpheron/chiaro-oscuro@v1
        with:
          project-name: ${{ inputs.project_name }}
          description: ${{ inputs.description }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 🏗️ Technical Architecture

### Core Components

1. **LLM Integration**
   - Uses [Simon Willison's llm CLI](https://github.com/simonw/llm)
   - [Anthony Shaw's llm-github-models](https://github.com/tonybaloney/llm-github-models) plugin
   - Shell-based orchestration for maximum portability

2. **SVG Processing Pipeline**
   ```python
   # Extraction pattern matching
   svg_pattern = r"```(?:svg)?\s*(.*?)\s*```"
   
   # Validation ensures well-formed SVG
   - Proper XML structure
   - Valid viewBox attributes
   - Complete opening/closing tags
   ```

3. **Theme Generation**
   - Single LLM call generates both variants
   - Automatic contrast optimization
   - Semantic HTML5 picture element integration

### GitHub Models Configuration

```bash
# Authentication via GitHub token
export GITHUB_MODELS_KEY=$GITHUB_TOKEN

# Model invocation
llm prompt -m "github/gpt-4o-mini" < prompt.txt
```

## 📊 Technical Benefits

### Accessibility
- **Automated Contrast**: Ensures sufficient contrast for both themes
- **Semantic Markup**: Proper `<title>` and `<desc>` elements
- **Screen Reader Compatible**: Full accessibility metadata

### Performance
- **Vector Format**: Scalable without quality loss
- **Optimized Output**: Clean SVG with minimal overhead
- **No Runtime Dependencies**: Pure SVG, no JavaScript required

### Integration
- **Git-Native**: Version controlled assets
- **CI/CD Ready**: Integrates with existing workflows
- **Platform Agnostic**: Works with any GitHub repository

## 🔬 Implementation Details

### Prompt Engineering
The system uses structured prompts to ensure consistent output:
```
OUTPUT FORMAT:
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>{{PROJECT_NAME}} Logo (Light Theme)</title>
  <desc>Logo optimized for light backgrounds</desc>
  <!-- SVG content -->
</svg>
```

### Error Handling
- Retry logic for LLM timeouts
- Fallback patterns for extraction
- Validation pipeline prevents malformed output

### Security
- No external API keys required
- Sandboxed execution environment
- Read-only model access

## 🚦 Continuous AI Roadmap

### Current Implementation
- [x] Basic SVG generation from text
- [x] Light/dark theme variants
- [x] GitHub Actions integration
- [x] PR-based review workflow

### Future Continuous AI Patterns
- [ ] **Continuous Optimization**: Auto-minimize SVG output
- [ ] **Continuous Validation**: Automated accessibility testing
- [ ] **Continuous Formats**: Generate PNG/WebP from master SVG
- [ ] **Continuous Metadata**: Semantic asset tagging

## 🤝 Contributing to Continuous AI

This project demonstrates how to build Continuous AI workflows on GitHub. Key principles:

1. **Use Platform Features**: GitHub Actions + Models
2. **Maintain Auditability**: Git history for all changes
3. **Enable Human Review**: PR workflow for oversight
4. **Focus on Automation**: Reduce repetitive technical tasks

### Development

```bash
# Clone and setup
git clone https://github.com/jmcpheron/chiaro-oscuro.git
cd chiaro-oscuro
uv sync

# Run tests
uv run pytest

# Local testing
export GITHUB_MODELS_KEY="your-github-token"
uv run python -m src.process_logos_llm
```

## 📚 Resources

- [Continuous AI at GitHub Next](https://githubnext.com/projects/continuous-ai/)
- [GitHub Models Documentation](https://github.com/marketplace/models)
- [LLM CLI Framework](https://llm.datasette.io/)
- [GitHub Actions AI Inference](https://github.com/actions/ai-inference)

## 📄 License

MIT © 2025 Jason McPheron

---

<div align="center">

Part of the **Continuous AI** ecosystem for software automation

[![Continuous AI](https://img.shields.io/badge/Learn%20More-Continuous%20AI-blue)](https://githubnext.com/projects/continuous-ai/)

</div>