<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.svg">
    <img src="assets/logo.png" alt="chiaro-oscuro logo" width="200">
  </picture>
</p>

# chiaro-oscuro 🌓

**Automatically optimize your repository logos for light and dark themes using AI**

## ✨ See It In Action

**chiaro-oscuro** takes your existing logo and creates optimized variants for both light and dark themes:

<div align="center">

| Light Theme | Dark Theme |
|-------------|------------|
| <img src="assets/logo-light.svg" alt="Light theme logo" width="120"> | <img src="assets/logo-dark.svg" alt="Dark theme logo" width="120"> |
| **Perfect for light backgrounds** | **Perfect for dark backgrounds** |
| High contrast, dark elements | High contrast, light elements |

</div>


## 🔧 Troubleshooting

### "GitHub Actions is not permitted to create or approve pull requests"

**Solution**: Enable PR creation in your repository:
1. Go to your repository **Settings**
2. Navigate to **Actions** > **General**  
3. Scroll to **Workflow permissions**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**


### "Models permission required"

**Solution**: Add the `models: read` permission to your workflow:
```yaml
permissions:
  contents: write
  pull-requests: write
  models: read  # ← Required for GitHub Models
```

## 📄 License

MIT © 2025 Jason McPheron


```markdown
[![Logo optimized by chiaro-oscuro](https://img.shields.io/badge/logo-chiaro--oscuro-blue)](https://github.com/jmcpheron/chiaro-oscuro)
```