# Code Animation Studio 🎬

A high-performance code animation tool that transforms your source code into beautiful typing animation videos using GPU-accelerated Skia rendering. Create stunning programming tutorials, presentations, and showcase videos with realistic typing effects and professional syntax highlighting.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Performance](https://img.shields.io/badge/Performance-50x_Faster-orange)
![Rendering](https://img.shields.io/badge/Engine-Skia_GPU-red)

## 📺 Demo Video

[![Code Animation Studio Demo](https://img.youtube.com/vi/WReYB3yGmgg/maxresdefault.jpg)](https://www.youtube.com/watch?v=WReYB3yGmgg)
*Click to watch the demo video on YouTube*

## ✨ Features

### 🚀 Blazing Fast Performance
- **GPU-accelerated rendering** with Skia engine
- **50x faster** than traditional animation libraries
- Real-time performance estimates
- Optimized memory management for long videos

### 🎨 Beautiful Themes
10 professional color themes included:
- Monokai
- Dracula
- GitHub Dark
- VS Code Dark
- Solarized Dark
- One Dark
- Nord
- Gruvbox Dark
- Tokyo Night
- Material Ocean

### 📝 Extensive Language Support
Support for **150+ programming languages** via Pygments:
- Popular: Python, JavaScript, TypeScript, Java, C++, Go, Rust
- Web: HTML, CSS, React (JSX/TSX)
- Mobile: Swift, Kotlin, Dart
- Data: SQL, JSON, YAML, XML
- And many more...

### 🎯 Quality Levels

| Quality | FPS | Features | Speed | Use Case |
|---------|-----|----------|-------|----------|
| **Low** | 30 | Basic rendering | ~230 fps | Quick previews |
| **Medium** | 30 | Antialiasing | ~215 fps | Drafts |
| **High** | 60 | Motion blur, shadows | ~150 fps | Professional videos |
| **Ultra** | 60 | 2x supersampling | ~100 fps | Maximum quality |

### 🔧 Advanced Features
- **Automatic scrolling** for long code files
- **Line numbers** display (optional)
- **Customizable typing speed** (5-200 chars/sec)
- **Auto font sizing** based on resolution
- **Word wrapping** for long lines
- **Realistic cursor animation** with blinking
- **Emoji support** 🎉

## 📦 Installation

### Requirements
- Python 3.7+
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `numpy` - Array operations
- `opencv-python` - Video encoding
- `skia-python` - Skia GPU rendering
- `Pygments` - Syntax highlighting
- `tkinter` - GUI interface (usually pre-installed)

## 🚀 Usage

### GUI Mode (Recommended)

```bash
python gui.py
```

The GUI provides:
- Visual code editor with syntax highlighting
- Real-time performance estimates
- Quality presets with visual feedback
- Theme preview
- Sample code templates
- Progress tracking

### CLI Mode

Basic usage:
```bash
python cli.py input.py -o output.mp4
```

Advanced options:
```bash
python cli.py code.js \
  --quality ultra \
  --speed 20 \
  --theme dracula \
  --size 2560x1440 \
  --fps 60
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output video file | `code_animation.mp4` |
| `-q, --quality` | Quality level (low/medium/high/ultra) | `high` |
| `-l, --language` | Programming language | Auto-detect |
| `-s, --speed` | Typing speed (chars/sec) | `15` |
| `-t, --theme` | Color theme | `monokai` |
| `--font-size` | Font size in pixels | Auto |
| `--size` | Video resolution | `1920x1080` |
| `--fps` | Frames per second | `60` |

## 📊 Performance

Rendering speed for 100 lines of code:

| Resolution | Low | Medium | High | Ultra |
|------------|-----|--------|------|-------|
| **720p** | ~1.5s | ~1.8s | ~3s | ~4.5s |
| **1080p** | ~2s | ~2.4s | ~4s | ~6s |
| **1440p** | ~2.5s | ~3s | ~5s | ~7.5s |
| **4K** | ~4s | ~4.8s | ~8s | ~12s |

## 🏗️ Architecture

### Core Components

#### `render.py`
The heart of the application - GPU-accelerated rendering engine:
- Skia-based drawing operations
- Token-based syntax highlighting
- Smooth scrolling algorithm
- Frame generation pipeline

#### `gui.py`
Tkinter-based desktop application:
- Interactive code editor
- Real-time configuration
- Visual feedback
- Progress tracking

#### `cli.py`
Command-line interface:
- Batch processing
- Automation friendly
- Full feature access

### Rendering Pipeline

```
Code Input → Tokenization → Syntax Highlighting → Frame Rendering → Video Encoding
     ↓            ↓                ↓                    ↓              ↓
   String     Pygments        Token Colors      Skia GPU Canvas    MP4 Output
```

## 🎨 Theme Structure

Themes are defined as dictionaries with color mappings:

```python
{
    "background": 0xFF272822,  # Editor background
    "text": 0xFFF8F8F2,        # Default text
    "cursor": 0xFFF8F8F2,      # Cursor color
    "colors": {
        Token.Keyword: 0xFFF92672,      # Keywords
        Token.String: 0xFFE6DB74,       # Strings
        Token.Comment: 0xFF75715E,      # Comments
        # ... more token mappings
    }
}
```

## 💡 Tips & Tricks

### Optimal Settings

**For Tutorials:**
- Quality: High
- Speed: 15-20 chars/sec
- Theme: Monokai or Dracula
- Show line numbers: Yes

**For Presentations:**
- Quality: Ultra
- Speed: 30-40 chars/sec
- Resolution: Match projector
- Theme: GitHub Dark or VS Code Dark

**For Social Media:**
- Resolution: 1080x1080 (square)
- Quality: Medium-High
- Speed: 25-30 chars/sec
- Theme: Tokyo Night or Nord

### Performance Optimization

1. **For long code files** (500+ lines):
   - Use Medium quality for faster rendering
   - Consider splitting into multiple videos
   - Increase typing speed to reduce duration

2. **For high resolutions** (4K):
   - High quality is usually sufficient
   - Ultra quality significantly increases render time
   - Auto font sizing ensures readability

3. **Memory usage**:
   - The tool uses ~500MB RAM for 1080p
   - 4K Ultra may use up to 2GB RAM
   - Long videos are processed in chunks

## 🛠️ Development

### Project Structure

```
code-animation-studio/
├── render.py            # Core rendering engine
├── gui.py               # GUI application
├── cli.py               # CLI interface
├── requirements.txt     # Dependencies
├── CLAUDE.md           # AI assistant instructions
└── README.md           # This file
```

### Key Classes

- `ModernCodeRenderer`: Main rendering engine
- `RenderConfig`: Configuration dataclass
- `CodeAnimationStudioGUI`: GUI application class

### Adding New Themes

Add your theme to the `THEMES` dictionary in `render.py`:

```python
THEMES["my_theme"] = {
    "background": 0xFF000000,
    "text": 0xFFFFFFFF,
    "cursor": 0xFFFFFFFF,
    "colors": {
        # Token color mappings
    }
}
```

## 🐛 Troubleshooting

### Common Issues

**Video not playing:**
- Ensure MP4 codec is installed
- Try a different video player
- Check file permissions

**Slow rendering:**
- Lower the quality setting
- Reduce resolution
- Increase typing speed
- Close other GPU-intensive applications

**Memory errors:**
- Use lower quality for long videos
- Reduce resolution
- Process in smaller chunks

**Font issues:**
- Install Monaco (macOS) or Consolas (Windows)
- Use `--font` flag to specify available font

## 📈 Benchmarks

Comparison with other tools (100 lines, 1080p, High quality):

| Tool | Render Time | Quality | GPU Support |
|------|-------------|---------|-------------|
| **Code Animation Studio** | **3-5s** | Excellent | ✅ |
| Manim | 150-200s | Good | ❌ |
| After Effects (manual) | 600s+ | Excellent | ✅ |
| PowerPoint Recording | 300s+ | Poor | ❌ |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional themes
- [ ] More transition effects
- [ ] Audio synchronization
- [ ] Live preview in GUI
- [ ] Cloud rendering support
- [ ] Browser-based version

## 📄 License

MIT License - feel free to use in commercial projects!

## 🙏 Acknowledgments

- **Skia** - GPU rendering engine
- **Pygments** - Syntax highlighting
- **OpenCV** - Video encoding
- All theme creators and open-source contributors

## 🔗 Links

- [Report Issues](https://github.com/enxgin/code-animation-studio/issues)
- [Request Features](https://github.com/enxgin/code-animation-studio/discussions)

---

**Made with ❤️ for developers, educators, and content creators**

*Transform your code into cinematic experiences!* 🎬✨