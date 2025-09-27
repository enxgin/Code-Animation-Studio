#!/usr/bin/env python3
"""
Code Animation Studio - CLI Interface
Modern Skia-based renderer ile yeniden yazılmış CLI
"""

import argparse
import sys
from pathlib import Path
from render import ModernCodeRenderer, RenderConfig


def main():
    parser = argparse.ArgumentParser(
        description="Code Animation Studio - Generate beautiful code animation videos with Skia GPU rendering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s code.py -o output.mp4
  %(prog)s code.js -q ultra -s 20
  %(prog)s code.rs -q low --fps 30 --size 1280x720

Quality Levels:
  low    : Fast rendering, 30fps, no antialiasing
  medium : Balanced, 30fps with antialiasing
  high   : Quality mode, 60fps with motion blur (default)
  ultra  : Maximum quality, 60fps with 2x supersampling
        """
    )

    # Input file
    parser.add_argument('input', help='Input code file')

    # Output
    parser.add_argument('-o', '--output', default='code_animation.mp4',
                      help='Output video file (default: code_animation.mp4)')

    # Quality
    parser.add_argument('-q', '--quality',
                      choices=['low', 'medium', 'high', 'ultra'],
                      default='high',
                      help='Video quality level (default: high)')

    # Language
    parser.add_argument('-l', '--language',
                      help='Programming language (auto-detect if not specified)')

    # Typing speed
    parser.add_argument('-s', '--speed', type=float, default=15.0,
                      help='Typing speed in characters per second (default: 15)')

    # Theme
    parser.add_argument('-t', '--theme',
                      choices=['monokai', 'dracula', 'github_dark', 'vscode_dark', 'solarized_dark',
                               'one_dark', 'nord', 'gruvbox_dark', 'tokyo_night', 'material_ocean'],
                      default='monokai',
                      help='Color theme (default: monokai)')

    # Font size
    parser.add_argument('--font-size', type=int, default=None,
                      help='Font size in pixels (auto-calculated if not specified)')

    # Auto font size
    parser.add_argument('--auto-font', action='store_true', default=True,
                      help='Automatically calculate font size based on resolution (default: True)')
    parser.add_argument('--no-auto-font', dest='auto_font', action='store_false',
                      help='Disable automatic font size calculation')

    # Font family
    parser.add_argument('--font', default='Monaco',
                      help='Font family (default: Monaco)')

    # Video dimensions
    parser.add_argument('--size', default='1920x1080',
                      help='Video size WIDTHxHEIGHT (default: 1920x1080)')

    # FPS
    parser.add_argument('--fps', type=int, default=60,
                      help='Frames per second (default: 60)')

    # Parse arguments
    args = parser.parse_args()

    # Check input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)

    # Read code
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Auto-detect language if not specified
    if not args.language:
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.lua': 'lua',
            '.dart': 'dart',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.sh': 'bash',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.md': 'markdown'
        }
        language = ext_to_lang.get(input_path.suffix.lower(), 'text')
    else:
        language = args.language

    # Parse video size
    try:
        width, height = map(int, args.size.split('x'))
    except:
        print(f"Error: Invalid size format '{args.size}'. Use WIDTHxHEIGHT (e.g., 1920x1080)")
        sys.exit(1)

    # Create config
    config = RenderConfig(
        width=width,
        height=height,
        fps=args.fps,
        quality=args.quality,
        font_size=args.font_size,  # None if not specified
        font_family=args.font,
        typing_speed=args.speed,
        theme=args.theme,
        auto_font_size=args.auto_font if args.font_size is None else False
    )

    # Create renderer
    print(f"\n🎬 Code Animation Studio - Skia GPU Renderer")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Input:    {input_path.name}")
    print(f"Language: {language}")
    print(f"Theme:    {args.theme}")
    print(f"Quality:  {args.quality}")
    print(f"Size:     {width}x{height}")
    print(f"FPS:      {args.fps}")
    print(f"Speed:    {args.speed} chars/sec")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # Generate video
    try:
        # Create output directory if not exists
        import os
        os.makedirs("output", exist_ok=True)

        # Prepare output path
        if os.path.dirname(args.output):
            # If user specified a path, use it as is
            output_path = args.output
        else:
            # If just filename, put in output folder
            output_path = os.path.join("output", args.output)

        renderer = ModernCodeRenderer(config)
        renderer.create_animation(
            code=code,
            language=language,
            output_path=output_path
        )

        print(f"\n✅ Video successfully created: {output_path}")

        # Show file size
        output_size = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"📁 File size: {output_size:.1f} MB")

    except Exception as e:
        print(f"\n❌ Error creating video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()