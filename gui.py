#!/usr/bin/env python3
"""
Code Animation Studio - GUI Interface
Modern GPU-accelerated renderer ile yeniden yazılmış GUI
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import sys
import os
import re

# Modern renderer'ı import et
from render import ModernCodeRenderer, RenderConfig

# Syntax highlighting için
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name
from pygments.token import Token
from pygments.styles import get_style_by_name


# Translation dictionary for multi-language support
TRANSLATIONS = {
    'en': {
        'title': 'Code Animation Studio',
        'code_editor': 'Code Editor',
        'open': '📁 Open',
        'save': '💾 Save',
        'clear': '🗑️ Clear',
        'language': 'Language:',
        'sample_codes': 'Sample Codes:',
        'video_settings': 'Video Settings',
        'quality_level': '🎯 Quality Level:',
        'quality_low': '⚡ Low - Very Fast (30fps, no AA)',
        'quality_medium': '🔧 Medium - Fast (30fps, with AA)',
        'quality_high': '🎬 High - Quality (60fps, motion blur)',
        'quality_ultra': '💎 Ultra - Maximum (60fps, 2x supersampling)',
        'typing_speed': 'Typing Speed:',
        'theme': 'Theme:',
        'font_size': 'Font Size:',
        'auto': 'Auto',
        'line_numbers': 'Line Numbers:',
        'show_line_numbers': 'Show line numbers in video',
        'video_size': 'Video Size:',
        'output_file': 'Output File:',
        'estimated_time': 'Estimated Processing Time:',
        'ready': 'Ready',
        'generate_video': '🚀 Generate Video',
        'open_output_folder': '📂 Open Output Folder',
        'chars_per_sec': 'chars/sec',
        'file_loaded': 'File loaded',
        'file_saved': 'File saved',
        'editor_cleared': 'Editor cleared',
        'sample_loaded': 'Sample code loaded',
        'warning': 'Warning',
        'error': 'Error',
        'success': 'Success',
        'confirm': 'Confirm',
        'confirm_clear': 'The code in the editor will be deleted. Are you sure?',
        'enter_code': 'Please enter code!',
        'video_preparing': '🚀 Preparing video... (Estimated: {time} seconds)',
        'video_progress': '🎬 {quality} Quality | Frame: {current}/{total} ({percentage}%)',
        'video_ready': '✅ Video ready: {filename} ({size} MB)',
        'video_created': 'Video successfully created!\n\n📁 File: {filename}\n💾 Size: {size} MB\n🎯 Quality: {quality} ({desc})\n\nFull path: {path}',
        'quality_desc_low': 'Quick preview',
        'quality_desc_medium': 'Balanced quality',
        'quality_desc_high': 'Professional quality',
        'quality_desc_ultra': 'Maximum quality',
        'performance_info': '{quality} quality {lines} lines ≈ {time} seconds',
        'performance_warning': '(may take longer)',
        'open_file': 'Select Code File',
        'save_file_dialog': 'Save Code',
        'file_open_error': 'Could not open file: {error}',
        'file_save_error': 'Could not save file: {error}',
        'video_create_error': 'Could not create video:\n{error}\n\nDetails in terminal.',
        'ui_language': '🌐 Interface:',
        'fps': 'FPS:',
        'all_files': 'All Files'
    },
    'tr': {
        'title': 'Kod Animasyon Stüdyosu',
        'code_editor': 'Kod Editörü',
        'open': '📁 Aç',
        'save': '💾 Kaydet',
        'clear': '🗑️ Temizle',
        'language': 'Dil:',
        'sample_codes': 'Örnek Kodlar:',
        'video_settings': 'Video Ayarları',
        'quality_level': '🎯 Kalite Seviyesi:',
        'quality_low': '⚡ Düşük - Çok Hızlı (30fps, AA yok)',
        'quality_medium': '🔧 Orta - Hızlı (30fps, AA ile)',
        'quality_high': '🎬 Yüksek - Kaliteli (60fps, hareket bulanıklığı)',
        'quality_ultra': '💎 Ultra - Maksimum (60fps, 2x süper örnekleme)',
        'typing_speed': 'Yazma Hızı:',
        'theme': 'Tema:',
        'font_size': 'Font Boyutu:',
        'auto': 'Otomatik',
        'line_numbers': 'Satır Numaraları:',
        'show_line_numbers': "Video'da satır numaralarını göster",
        'video_size': 'Video Boyutu:',
        'output_file': 'Çıktı Dosyası:',
        'estimated_time': 'Tahmini İşlem Süresi:',
        'ready': 'Hazır',
        'generate_video': '🚀 Video Oluştur',
        'open_output_folder': '📂 Çıktı Klasörünü Aç',
        'chars_per_sec': 'karakter/sn',
        'file_loaded': 'Dosya yüklendi',
        'file_saved': 'Dosya kaydedildi',
        'editor_cleared': 'Editör temizlendi',
        'sample_loaded': 'Örnek kod yüklendi',
        'warning': 'Uyarı',
        'error': 'Hata',
        'success': 'Başarılı',
        'confirm': 'Onayla',
        'confirm_clear': 'Editördeki kod silinecek. Emin misiniz?',
        'enter_code': 'Lütfen kod girin!',
        'video_preparing': '🚀 Video hazırlanıyor... (Tahmini: {time} saniye)',
        'video_progress': '🎬 {quality} Kalite | Kare: {current}/{total} ({percentage}%)',
        'video_ready': '✅ Video hazır: {filename} ({size} MB)',
        'video_created': 'Video başarıyla oluşturuldu!\n\n📁 Dosya: {filename}\n💾 Boyut: {size} MB\n🎯 Kalite: {quality} ({desc})\n\nTam yol: {path}',
        'quality_desc_low': 'Hızlı önizleme',
        'quality_desc_medium': 'Dengeli kalite',
        'quality_desc_high': 'Profesyonel kalite',
        'quality_desc_ultra': 'Maksimum kalite',
        'performance_info': '{quality} kalitede {lines} satır ≈ {time} saniye',
        'performance_warning': '(uzun sürebilir)',
        'open_file': 'Kod Dosyası Seç',
        'save_file_dialog': 'Kodu Kaydet',
        'file_open_error': 'Dosya açılamadı: {error}',
        'file_save_error': 'Dosya kaydedilemedi: {error}',
        'video_create_error': 'Video oluşturulamadı:\n{error}\n\nDetaylar terminalde.',
        'ui_language': '🌐 Arayüz:',
        'fps': 'FPS:',
        'all_files': 'Tüm Dosyalar'
    }
}


class CodeAnimationStudioGUI:
    """Ana GUI uygulaması - Modern GPU renderer ile"""

    def __init__(self, root):
        self.root = root

        # Default language is English
        self.current_language = 'en'
        self.translations = TRANSLATIONS[self.current_language]

        self.root.title(self.translations['title'])
        self.root.geometry("1200x800")

        # Syntax highlighting state
        self.current_theme = "monokai"
        self.syntax_enabled = True
        self.debug_mode = False  # Debug disabled for performance
        self.highlighting_timer = None  # Debounce timer for syntax highlighting

        # Stil ayarları
        self.setup_styles()

        # Ana frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Sol panel - Kod editörü
        self.create_editor_panel(main_frame)

        # Sağ panel - Ayarlar
        self.create_settings_panel(main_frame)

        # Alt panel - Kontroller ve durum
        self.create_control_panel(main_frame)

        # Grid ağırlıkları
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Varsayılan değerleri yükle
        self.load_defaults()

    def setup_styles(self):
        """Tema ve stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')

        # Renk şeması
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 11, 'bold'))
        style.configure('Generate.TButton', font=('Arial', 12, 'bold'))

    def create_editor_panel(self, parent):
        """Sol panel - Kod editörü"""
        self.editor_frame = ttk.LabelFrame(parent, text=self.translations['code_editor'], padding="10")
        self.editor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Toolbar - Grid layout for better control
        toolbar = ttk.Frame(self.editor_frame)
        toolbar.pack(fill='x', pady=(0, 5), expand=False)
        toolbar.columnconfigure(6, weight=1)  # Make language combo column expandable

        # Use grid layout for toolbar elements
        self.open_btn = ttk.Button(toolbar, text=self.translations['open'], command=self.open_file, width=8)
        self.open_btn.grid(row=0, column=0, padx=2)

        self.save_btn = ttk.Button(toolbar, text=self.translations['save'], command=self.save_file, width=8)
        self.save_btn.grid(row=0, column=1, padx=2)

        self.clear_btn = ttk.Button(toolbar, text=self.translations['clear'], command=self.clear_editor, width=8)
        self.clear_btn.grid(row=0, column=2, padx=2)

        # Language selector for UI (Turkish/English)
        self.ui_lang_label = ttk.Label(toolbar, text=self.translations['ui_language'])
        self.ui_lang_label.grid(row=0, column=3, padx=(20, 5))
        self.ui_language_var = tk.StringVar(value='en')
        ui_language_combo = ttk.Combobox(
            toolbar,
            textvariable=self.ui_language_var,
            values=['Türkçe', 'English'],
            width=10,
            state='readonly'
        )
        ui_language_combo.grid(row=0, column=4, padx=(0, 15), sticky='w')
        ui_language_combo.bind('<<ComboboxSelected>>', self.change_ui_language)
        ui_language_combo.set('English')

        # Programming language selection
        self.lang_label = ttk.Label(toolbar, text=self.translations['language'])
        self.lang_label.grid(row=0, column=5, padx=(0, 5))
        self.language_var = tk.StringVar(value="python")
        language_combo = ttk.Combobox(
            toolbar,
            textvariable=self.language_var,
            values=["python", "javascript", "java", "cpp", "csharp", "go", "rust", "typescript", "swift", "kotlin", "php", "ruby", "html", "css", "sql"],
            width=20,
            state='readonly'
        )
        language_combo.grid(row=0, column=6, padx=(0, 15), sticky='ew')

        # Kod editörü - Word wrap enabled for long lines
        self.code_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,  # Changed from tk.NONE to tk.WORD for line wrapping
            font=('Monaco', 11) if sys.platform == 'darwin' else ('Consolas', 11),
            bg='#1E1E1E',
            fg='#F8F8F2',
            insertbackground='white',
            selectbackground='#3E7B91',
            height=30
        )
        self.code_editor.pack(fill='both', expand=True)

        # Flicker önleme için optimizasyonlar
        self.code_editor.configure(
            autoseparators=False,  # Undo history optimizasyonu
            blockcursor=False,     # Cursor flicker önleme
            padx=5,               # Sol boşluk için
            pady=5                # Üst boşluk için
        )

        # Event bindings for syntax highlighting - daha kapsamlı
        self.code_editor.bind('<KeyRelease>', self.on_text_change)
        self.code_editor.bind('<KeyPress>', self.on_text_change)
        self.code_editor.bind('<Button-1>', self.on_text_change)
        self.code_editor.bind('<ButtonRelease-1>', self.on_text_change)
        self.code_editor.bind('<FocusIn>', self.on_text_change)

        # Paste event bindings - all platforms and methods
        self.code_editor.bind('<<Paste>>', self.on_paste_change)  # Virtual event - catches all paste methods
        self.code_editor.bind('<Control-v>', self.on_paste_change)  # Windows/Linux
        self.code_editor.bind('<Command-v>', self.on_paste_change)  # macOS
        self.code_editor.bind('<Control-V>', self.on_paste_change)  # Uppercase variant
        self.code_editor.bind('<Command-V>', self.on_paste_change)  # macOS uppercase

        self.code_editor.bind('<Control-a>', self.on_text_change)  # Select all
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        # Modified flag monitoring for text changes
        self.code_editor.edit_modified(False)
        self.root.after(100, self.check_for_changes)

        # Initialize syntax highlighting (delayed to avoid errors)
        self.root.after(100, self.initialize_syntax_highlighting)

        # Örnek kodlar
        self.create_sample_codes(self.editor_frame)

    def create_sample_codes(self, parent):
        """Örnek kod şablonları"""
        sample_frame = ttk.Frame(parent)
        sample_frame.pack(fill='x', pady=(5, 0))

        self.sample_label = ttk.Label(sample_frame, text=self.translations['sample_codes'])
        self.sample_label.pack(side='left', padx=(0, 5))

        samples = {
            "Python AI": self.get_ai_code,
            "JavaScript React": self.get_react_code,
            "TypeScript Class": self.get_ts_code,
            "Rust System": self.get_rust_code
        }

        for name, func in samples.items():
            ttk.Button(
                sample_frame,
                text=name,
                command=lambda f=func: self.load_sample_code(f)
            ).pack(side='left', padx=2)

    def create_settings_panel(self, parent):
        """Sağ panel - Ayarlar"""
        self.settings_frame = ttk.LabelFrame(parent, text=self.translations['video_settings'], padding="10")
        self.settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Video Kalitesi - EN ÖNEMLİ
        self.quality_heading = ttk.Label(self.settings_frame, text=self.translations['quality_level'], style='Heading.TLabel')
        self.quality_heading.grid(row=0, column=0, sticky='w', pady=10)
        self.quality_var = tk.StringVar(value="high")
        quality_frame = ttk.Frame(self.settings_frame)
        quality_frame.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky='w')

        qualities = [
            (self.translations['quality_low'], "low"),
            (self.translations['quality_medium'], "medium"),
            (self.translations['quality_high'], "high"),
            (self.translations['quality_ultra'], "ultra")
        ]

        # Store radio buttons for later updates
        self.quality_radios = {}
        for text, value in qualities:
            rb = ttk.Radiobutton(
                quality_frame,
                text=text,
                variable=self.quality_var,
                value=value
            )
            rb.pack(anchor='w', pady=2)
            self.quality_radios[value] = rb
            if value == "high":
                rb.configure(style='Selected.TRadiobutton')

        # Separator
        ttk.Separator(self.settings_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        # Yazma Hızı
        self.speed_label_text = ttk.Label(self.settings_frame, text=self.translations['typing_speed'])
        self.speed_label_text.grid(row=3, column=0, sticky='w', pady=5)
        speed_frame = ttk.Frame(self.settings_frame)
        speed_frame.grid(row=3, column=1, pady=5, padx=5, sticky='w')

        self.typing_speed_var = tk.DoubleVar(value=30.0)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=5.0,
            to=200.0,
            variable=self.typing_speed_var,
            orient='horizontal',
            length=200
        )
        speed_scale.pack(side='left')

        self.speed_label = ttk.Label(speed_frame, text=f"30 {self.translations['chars_per_sec']}", width=20)
        self.speed_label.pack(side='left', padx=5)
        speed_scale.configure(command=self.update_speed_label)

        # Tema seçimi
        self.theme_label = ttk.Label(self.settings_frame, text=self.translations['theme'])
        self.theme_label.grid(row=4, column=0, sticky='w', pady=5)
        self.theme_var = tk.StringVar(value="monokai")
        theme_combo = ttk.Combobox(
            self.settings_frame,
            textvariable=self.theme_var,
            values=["monokai", "dracula", "github_dark", "vscode_dark", "solarized_dark",
                    "one_dark", "nord", "gruvbox_dark", "tokyo_night", "material_ocean"],
            state='readonly',
            width=25
        )
        theme_combo.grid(row=4, column=1, pady=5, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)

        # Font boyutu
        self.font_label = ttk.Label(self.settings_frame, text=self.translations['font_size'])
        self.font_label.grid(row=5, column=0, sticky='w', pady=5)
        font_frame = ttk.Frame(self.settings_frame)
        font_frame.grid(row=5, column=1, pady=5, padx=5, sticky='w')

        self.auto_font_var = tk.BooleanVar(value=True)
        self.auto_check = ttk.Checkbutton(
            font_frame,
            text=self.translations['auto'],
            variable=self.auto_font_var,
            command=self.toggle_font_spinbox
        )
        auto_check = self.auto_check
        auto_check.pack(side='left', padx=(0, 10))

        self.font_size_var = tk.IntVar(value=24)
        self.font_spinbox = ttk.Spinbox(
            font_frame,
            from_=14,
            to=64,
            increment=2,
            textvariable=self.font_size_var,
            width=10,
            state='disabled'
        )
        self.font_spinbox.pack(side='left')

        self.font_size_label = ttk.Label(font_frame, text="px")
        self.font_size_label.pack(side='left', padx=(5, 0))

        # Satır numaraları göster/gizle
        self.line_num_label = ttk.Label(self.settings_frame, text=self.translations['line_numbers'])
        self.line_num_label.grid(row=6, column=0, sticky='w', pady=5)
        self.show_line_numbers_var = tk.BooleanVar(value=False)
        self.line_num_check = ttk.Checkbutton(
            self.settings_frame,
            text=self.translations['show_line_numbers'],
            variable=self.show_line_numbers_var
        )
        self.line_num_check.grid(row=6, column=1, pady=5, padx=5, sticky='w')

        # Separator for Scroll Settings
        ttk.Separator(self.settings_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky='ew', pady=10)

        # Video boyutları
        self.video_size_label = ttk.Label(self.settings_frame, text=self.translations['video_size'])
        self.video_size_label.grid(row=8, column=0, sticky='w', pady=5)
        self.resolution_var = tk.StringVar(value="1920x1080")
        resolution_combo = ttk.Combobox(
            self.settings_frame,
            textvariable=self.resolution_var,
            values=["1280x720", "1920x1080", "2560x1440", "3840x2160"],
            state='readonly',
            width=25
        )
        resolution_combo.grid(row=8, column=1, pady=5, padx=5)
        resolution_combo.bind('<<ComboboxSelected>>', lambda e: self.update_auto_font_display())

        # FPS
        self.fps_label = ttk.Label(self.settings_frame, text=self.translations.get('fps', 'FPS:'))
        self.fps_label.grid(row=9, column=0, sticky='w', pady=5)
        self.fps_var = tk.IntVar(value=60)
        fps_combo = ttk.Combobox(
            self.settings_frame,
            textvariable=self.fps_var,
            values=[24, 30, 60],
            state='readonly',
            width=25
        )
        fps_combo.grid(row=9, column=1, pady=5, padx=5)

        # Çıktı dosyası
        self.output_label = ttk.Label(self.settings_frame, text=self.translations['output_file'])
        self.output_label.grid(row=10, column=0, sticky='w', pady=5)
        output_frame = ttk.Frame(self.settings_frame)
        output_frame.grid(row=10, column=1, pady=5, padx=5, sticky='w')

        self.output_var = tk.StringVar(value="code_animation")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=18)
        output_entry.pack(side='left')
        ttk.Label(output_frame, text=".mp4").pack(side='left')

        # Performans bilgisi
        self.perf_heading = ttk.Label(self.settings_frame, text=self.translations['estimated_time'], style='Heading.TLabel')
        self.perf_heading.grid(row=11, column=0, columnspan=2, sticky='w', pady=(20, 5))

        self.performance_label = ttk.Label(
            self.settings_frame,
            text=self.translations['performance_info'].format(quality='High', lines=100, time='3-5'),
            foreground='green'
        )
        self.performance_label.grid(row=12, column=0, columnspan=2, sticky='w', pady=5)

        # Quality değiştiğinde performans tahmini güncelle
        quality_frame.bind('<ButtonRelease-1>', lambda e: self.update_performance_estimate())

    def create_control_panel(self, parent):
        """Alt panel - Kontroller ve durum"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        # İlerleme çubuğu
        self.progress = ttk.Progressbar(control_frame, mode='determinate')
        self.progress.pack(fill='x', pady=(0, 5))

        # Durum etiketi
        self.status_label = ttk.Label(control_frame, text=self.translations['ready'], relief='sunken')
        self.status_label.pack(fill='x', pady=(0, 5))

        # Butonlar
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()

        self.generate_btn = ttk.Button(
            button_frame,
            text=self.translations['generate_video'],
            command=self.generate_video,
            style='Generate.TButton'
        )
        self.generate_btn.pack(side='left', padx=5)


        self.folder_btn = ttk.Button(
            button_frame,
            text=self.translations['open_output_folder'],
            command=self.open_output_folder
        )
        self.folder_btn.pack(side='left', padx=5)

    def update_speed_label(self, value):
        """Hız etiketi güncelleme"""
        speed = float(value)
        self.speed_label.config(text=f"{speed:.0f} {self.translations['chars_per_sec']}")
        self.update_performance_estimate()

    def change_ui_language(self, event=None):
        """Change the UI language between Turkish and English"""
        # Get selected language
        selected = self.ui_language_var.get()
        if selected == 'English':
            self.current_language = 'en'
        else:
            self.current_language = 'tr'

        # Update translations
        self.translations = TRANSLATIONS[self.current_language]

        # Update all UI elements
        self.update_ui_texts()

    def update_ui_texts(self):
        """Update all UI texts with current language"""
        # Window title
        self.root.title(self.translations['title'])

        # Editor panel
        self.editor_frame.config(text=self.translations['code_editor'])
        self.open_btn.config(text=self.translations['open'])
        self.save_btn.config(text=self.translations['save'])
        self.clear_btn.config(text=self.translations['clear'])
        self.ui_lang_label.config(text=self.translations['ui_language'])
        self.lang_label.config(text=self.translations['language'])
        self.sample_label.config(text=self.translations['sample_codes'])

        # Settings panel
        self.settings_frame.config(text=self.translations['video_settings'])
        self.quality_heading.config(text=self.translations['quality_level'])

        # Update quality radio buttons
        if hasattr(self, 'quality_radios'):
            self.quality_radios['low'].config(text=self.translations['quality_low'])
            self.quality_radios['medium'].config(text=self.translations['quality_medium'])
            self.quality_radios['high'].config(text=self.translations['quality_high'])
            self.quality_radios['ultra'].config(text=self.translations['quality_ultra'])

        self.speed_label_text.config(text=self.translations['typing_speed'])
        self.theme_label.config(text=self.translations['theme'])
        self.font_label.config(text=self.translations['font_size'])
        self.auto_check.config(text=self.translations['auto'])
        self.line_num_label.config(text=self.translations['line_numbers'])
        self.line_num_check.config(text=self.translations['show_line_numbers'])
        self.video_size_label.config(text=self.translations['video_size'])
        self.output_label.config(text=self.translations['output_file'])
        self.perf_heading.config(text=self.translations['estimated_time'])

        # Update FPS label if exists
        if hasattr(self, 'fps_label'):
            self.fps_label.config(text=self.translations.get('fps', 'FPS:'))

        # Control panel
        self.status_label.config(text=self.translations['ready'])
        self.generate_btn.config(text=self.translations['generate_video'])
        self.folder_btn.config(text=self.translations['open_output_folder'])

        # Update performance estimate
        self.update_performance_estimate()

    def toggle_font_spinbox(self):
        """Toggle font size spinbox based on auto checkbox"""
        if self.auto_font_var.get():
            self.font_spinbox.config(state='disabled')
            # Update label to show auto calculated size
            self.update_auto_font_display()
        else:
            self.font_spinbox.config(state='normal')

    def update_auto_font_display(self):
        """Update font size display when in auto mode"""
        if self.auto_font_var.get():
            from modern_renderer import calculate_auto_font_size
            width, height = map(int, self.resolution_var.get().split('x'))
            auto_size = calculate_auto_font_size(width, height)
            self.font_size_label.config(text=f"px (Auto: {auto_size}px)")

    def update_performance_estimate(self):
        """Performans tahminini güncelle"""
        quality = self.quality_var.get()
        lines = len(self.code_editor.get('1.0', tk.END).split('\n'))
        chars = len(self.code_editor.get('1.0', tk.END))
        typing_speed = self.typing_speed_var.get()

        # Tahmini süre hesapla
        duration_sec = chars / typing_speed

        # Quality'ye göre render hızı (yaklaşık)
        speed_multiplier = {
            "low": 0.5,
            "medium": 0.6,
            "high": 1.0,
            "ultra": 1.5
        }

        render_time = duration_sec * speed_multiplier.get(quality, 1.0)

        if render_time < 5:
            color = 'green'
            text = self.translations['performance_info'].format(
                quality=quality.title(),
                lines=lines,
                time=f'{render_time:.1f}'
            )
        elif render_time < 15:
            color = 'orange'
            text = self.translations['performance_info'].format(
                quality=quality.title(),
                lines=lines,
                time=f'{render_time:.1f}'
            )
        else:
            color = 'red'
            text = self.translations['performance_info'].format(
                quality=quality.title(),
                lines=lines,
                time=f'{render_time:.1f}'
            ) + f" {self.translations['performance_warning']}"

        self.performance_label.config(text=text, foreground=color)

    def load_defaults(self):
        """Varsayılan değerleri yükle"""
        self.code_editor.insert('1.0', self.get_ai_code())
        self.update_performance_estimate()

        # Reset modified flag for initial load
        self.code_editor.edit_modified(False)

    def open_file(self):
        """Dosya aç"""
        file_path = filedialog.askopenfilename(
            title=self.translations['open_file'],
            filetypes=[
                ("Python", "*.py"),
                ("JavaScript", "*.js"),
                ("TypeScript", "*.ts"),
                ("Rust", "*.rs"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.code_editor.delete('1.0', tk.END)
                    self.code_editor.insert('1.0', content)

                # Dosya uzantısına göre dili ayarla
                ext = Path(file_path).suffix.lower()
                lang_map = {
                    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.rs': 'rust', '.java': 'java', '.cpp': 'cpp', '.go': 'go'
                }
                if ext in lang_map:
                    self.language_var.set(lang_map[ext])

                self.update_status(f"{self.translations['file_loaded']}: {Path(file_path).name}")
                self.update_performance_estimate()

                # Syntax highlighting'i trigger et
                if self.syntax_enabled:
                    self.root.after(200, self.highlight_syntax)
            except Exception as e:
                messagebox.showerror(self.translations['error'], self.translations['file_open_error'].format(error=e))

    def save_file(self):
        """Kodu dosyaya kaydet"""
        file_path = filedialog.asksaveasfilename(
            title=self.translations['save_file_dialog'],
            defaultextension=".py",
            filetypes=[
                ("Python", "*.py"),
                ("JavaScript", "*.js"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            try:
                content = self.code_editor.get('1.0', tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"{self.translations['file_saved']}: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror(self.translations['error'], self.translations['file_save_error'].format(error=e))

    def clear_editor(self):
        """Editörü temizle"""
        if messagebox.askyesno(self.translations['confirm'], self.translations['confirm_clear']):
            self.code_editor.delete('1.0', tk.END)
            self.update_status(self.translations['editor_cleared'])
            self.update_performance_estimate()

            # Clear syntax highlighting tags
            if self.syntax_enabled:
                for tag_name in self.syntax_tags.values():
                    self.code_editor.tag_remove(tag_name, '1.0', tk.END)

    def load_sample_code(self, code_func):
        """Örnek kod yükle"""
        self.code_editor.delete('1.0', tk.END)
        self.code_editor.insert('1.0', code_func())
        self.update_status(self.translations['sample_loaded'])
        self.update_performance_estimate()

        # Syntax highlighting'i trigger et
        if self.syntax_enabled:
            self.root.after(200, self.highlight_syntax)

    def generate_video(self):
        """Video oluştur (thread içinde)"""
        code = self.code_editor.get('1.0', tk.END).strip()

        if not code:
            messagebox.showwarning(self.translations['warning'], self.translations['enter_code'])
            return

        # Thread'de çalıştır
        thread = threading.Thread(target=self._generate_video_thread, args=(code,))
        thread.daemon = True
        thread.start()

    def _generate_video_thread(self, code):
        """Video oluşturma thread'i"""
        try:
            # UI güncelle
            self.generate_btn.config(state='disabled')
            self.progress.config(mode='indeterminate')
            self.progress.start()

            # Tahmini süre hesapla
            char_count = len(code)
            estimated_time = char_count / self.typing_speed_var.get()
            self.update_status(self.translations['video_preparing'].format(time=f'{estimated_time:.0f}'))

            # Config oluştur
            width, height = map(int, self.resolution_var.get().split('x'))
            config = RenderConfig(
                width=width,
                height=height,
                fps=self.fps_var.get(),
                quality=self.quality_var.get(),
                font_size=None if self.auto_font_var.get() else self.font_size_var.get(),
                typing_speed=self.typing_speed_var.get(),
                theme=self.theme_var.get(),
                auto_font_size=self.auto_font_var.get(),
                show_line_numbers=self.show_line_numbers_var.get(),  # Satır numaraları ayarı
                viewport_pixel_snap=True,  # Pixel snapping for stability
                hide_cursor_near_edges=True,  # Hide cursor near edges
                downscale_filter="area"  # Use stable downscale filter
            )

            # Renderer oluştur ve video üret
            renderer = ModernCodeRenderer(config)
            # Using optimized internal scroll settings

            # Create output directory if not exists
            import os
            os.makedirs("output", exist_ok=True)

            # Save video to output folder
            output_path = os.path.join("output", f"{self.output_var.get()}.mp4")

            # Progress callback için determinate mode'a geç
            self.progress.stop()
            self.progress.config(mode='determinate', value=0)

            # Video oluştur
            print(f"Creating video at: {output_path}")  # Debug

            # Progress callback function
            def update_progress(current_frame, total_frames, percentage):
                self.progress.config(value=percentage)
                quality_text = self.quality_var.get().upper()
                self.update_status(self.translations['video_progress'].format(
                    quality=quality_text,
                    current=current_frame,
                    total=total_frames,
                    percentage=f'{percentage:.0f}'
                ))
                self.root.update_idletasks()

            result = renderer.create_animation(
                code=code,
                language=self.language_var.get(),
                output_path=output_path,
                progress_callback=update_progress
            )

            # Biraz bekle - dosya yazımının tamamlanması için
            import time
            time.sleep(0.5)

            # Dosya varlığını kontrol et
            abs_path = os.path.abspath(output_path)
            print(f"Checking for video at: {abs_path}")  # Debug

            if os.path.exists(abs_path) or os.path.exists(output_path):
                actual_path = abs_path if os.path.exists(abs_path) else output_path
                file_size = os.path.getsize(actual_path) / (1024 * 1024)  # MB
                # Başarılı
                self.progress.config(value=100)
                self.update_status(self.translations['video_ready'].format(
                    filename=os.path.basename(actual_path),
                    size=f'{file_size:.1f}'
                ))

                # Kalite ve performans bilgisi
                quality_info = {
                    "low": self.translations['quality_desc_low'],
                    "medium": self.translations['quality_desc_medium'],
                    "high": self.translations['quality_desc_high'],
                    "ultra": self.translations['quality_desc_ultra']
                }
                quality_desc = quality_info.get(self.quality_var.get(), "")

                # Use root.after to show success message in main thread
                success_msg = self.translations['video_created'].format(
                    filename=os.path.basename(actual_path),
                    size=f'{file_size:.1f}',
                    quality=self.quality_var.get().upper(),
                    desc=quality_desc,
                    path=actual_path
                )
                self.root.after(0, lambda: messagebox.showinfo(self.translations['success'], success_msg))
            else:
                # Mevcut dizindeki mp4 dosyalarını listele
                mp4_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
                print(f"MP4 files in current directory: {mp4_files}")
                raise Exception(f"Video dosyası bulunamadı: {output_path}\nMevcut MP4 dosyaları: {mp4_files}")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error details: {error_details}")  # Terminal'de görmek için
            self.update_status(self.translations['error'])

            # Use root.after to show messagebox in main thread
            error_msg = self.translations['video_create_error'].format(error=str(e))
            self.root.after(0, lambda: messagebox.showerror(self.translations['error'], error_msg))

        finally:
            # UI'yi eski haline getir
            self.progress.stop()
            self.progress.config(value=0)
            self.generate_btn.config(state='normal')


    def open_output_folder(self):
        """Çıktı klasörünü aç"""
        import platform
        import subprocess

        output_dir = Path(".").absolute()

        system = platform.system()
        if system == "Windows":
            os.startfile(str(output_dir))
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(output_dir)])
        else:  # Linux
            subprocess.run(["xdg-open", str(output_dir)])

    def update_status(self, message):
        """Durum mesajını güncelle"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    # Örnek kod fonksiyonları
    def get_ai_code(self):
        return '''import torch
import torch.nn as nn

class TransformerModel(nn.Module):
    """Modern AI Transformer Architecture"""

    def __init__(self, vocab_size, d_model=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.Transformer(d_model)
        self.output = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x, x)
        return self.output(x)

# Initialize model
model = TransformerModel(vocab_size=10000)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")'''

    def get_react_code(self):
        self.language_var.set("javascript")
        return '''import React, { useState, useEffect } from 'react';

const AnimatedCounter = ({ target = 100 }) => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setCount(prev => {
                if (prev >= target) {
                    clearInterval(timer);
                    return target;
                }
                return prev + 1;
            });
        }, 10);

        return () => clearInterval(timer);
    }, [target]);

    return (
        <div className="counter">
            <h1>{count}</h1>
            <div className="progress-bar">
                <div style={{ width: `${(count/target)*100}%` }} />
            </div>
        </div>
    );
};

export default AnimatedCounter;'''

    def get_ts_code(self):
        self.language_var.set("typescript")
        return '''interface User {
    id: number;
    name: string;
    email: string;
    role: 'admin' | 'user' | 'guest';
}

class UserService {
    private users: Map<number, User> = new Map();

    async createUser(data: Omit<User, 'id'>): Promise<User> {
        const id = Date.now();
        const user: User = { ...data, id };

        this.users.set(id, user);

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 100));

        return user;
    }

    async getUser(id: number): Promise<User | undefined> {
        return this.users.get(id);
    }
}

const service = new UserService();
const newUser = await service.createUser({
    name: 'Alice',
    email: 'alice@example.com',
    role: 'admin'
});'''


    def get_rust_code(self):
        self.language_var.set("rust")
        return '''use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Clone)]
struct Cache<T> {
    data: Arc<RwLock<Vec<T>>>,
}

impl<T: Clone> Cache<T> {
    fn new() -> Self {
        Self {
            data: Arc::new(RwLock::new(Vec::new())),
        }
    }

    async fn insert(&self, item: T) {
        let mut data = self.data.write().await;
        data.push(item);
    }

    async fn get_all(&self) -> Vec<T> {
        let data = self.data.read().await;
        data.clone()
    }
}

#[tokio::main]
async fn main() {
    let cache = Cache::<String>::new();

    cache.insert("Rust".to_string()).await;
    cache.insert("is".to_string()).await;
    cache.insert("awesome!".to_string()).await;

    let items = cache.get_all().await;
    println!("Cache contents: {:?}", items);
}'''


    def get_theme_colors(self, theme_name):
        """Seçilen tema için renkleri döndür"""
        # Modern renderer'dan tema renklerini al
        try:
            from modern_renderer import THEMES
            if theme_name in THEMES:
                theme = THEMES[theme_name]
                return {
                    'bg': theme['background'],
                    'fg': theme.get('text', theme.get('foreground', 0xFFF8F8F2)),
                    'select_bg': theme.get('selection', '#3E7B91'),
                    'colors': theme.get('colors', theme)  # Some themes store colors directly
                }
        except Exception as e:
            print(f"Theme import error: {e}")

        # Fallback renkler
        return {
            'bg': 0xFF272822,  # Monokai dark
            'fg': 0xFFF8F8F2,  # Monokai light
            'select_bg': '#3E7B91',
            'colors': {
                Token.Keyword: 0xFFF92672,
                Token.String: 0xFFE6DB74,
                Token.Comment: 0xFF75715E,
                Token.Number: 0xFFAE81FF,
                Token.Name.Function: 0xFFA6E22E,
                Token.Name.Class: 0xFFA6E22E,
                Token.Operator: 0xFFF92672,
            }
        }

    def hex_from_int(self, color_int):
        """Integer color'u hex'e çevir"""
        # Color integer'ları hex string'e çevir
        if isinstance(color_int, int):
            r = (color_int >> 16) & 0xFF
            g = (color_int >> 8) & 0xFF
            b = color_int & 0xFF
            return f"#{r:02x}{g:02x}{b:02x}"
        return color_int

    def setup_syntax_tags(self):
        """Syntax highlighting için text widget tag'lerini oluştur - SIMPLIFIED"""
        # Clear existing tags
        for tag in ['keyword', 'string', 'comment', 'number', 'function', 'builtin', 'class']:
            try:
                self.code_editor.tag_delete(tag)
            except:
                pass

        # Simple color scheme
        colors = {
            'keyword': '#F92672',   # Pink/Red
            'string': '#E6DB74',    # Yellow
            'comment': '#75715E',   # Gray
            'number': '#AE81FF',    # Purple
            'function': '#A6E22E',  # Green
            'builtin': '#66D9EF',   # Cyan
            'class': '#A6E22E',     # Green
        }

        # Configure tags with colors
        for tag_name, color in colors.items():
            self.code_editor.tag_configure(tag_name, foreground=color)

    def highlight_syntax(self):
        """Kod editöründeki metni syntax highlighting ile renklendir - SIMPLIFIED"""
        if not self.syntax_enabled:
            return

        # Cancel any pending highlighting timer
        if hasattr(self, 'highlighting_timer') and self.highlighting_timer:
            self.root.after_cancel(self.highlighting_timer)
            self.highlighting_timer = None

        try:
            # Save cursor position to restore later
            insert_pos = self.code_editor.index("insert")

            # Get current text
            code = self.code_editor.get('1.0', tk.END)
            if not code.strip():
                return

            # Get language lexer
            language = self.language_var.get()
            try:
                lexer = get_lexer_by_name(language)
            except:
                return

            # Clear all tags (batch operation for speed)
            for tag in ['keyword', 'string', 'comment', 'number', 'function', 'builtin', 'class']:
                self.code_editor.tag_remove(tag, '1.0', tk.END)

            # Process tokens
            line_no = 1
            col_no = 0

            for token_type, text in lexer.get_tokens(code):
                # Handle newlines
                if '\n' in text:
                    newline_count = text.count('\n')
                    line_no += newline_count
                    if text.endswith('\n'):
                        col_no = 0
                    else:
                        # Text after last newline
                        col_no = len(text.split('\n')[-1])
                    continue

                # Calculate position
                start_pos = f"{line_no}.{col_no}"
                col_no += len(text)
                end_pos = f"{line_no}.{col_no}"

                # Skip whitespace
                if not text.strip():
                    continue

                # Simplified token matching
                tag_name = self.get_tag_for_token(token_type)
                if tag_name:
                    self.code_editor.tag_add(tag_name, start_pos, end_pos)

            # Restore cursor position
            self.code_editor.mark_set("insert", insert_pos)

            # Batch update to prevent flicker - ONLY update once at the end
            self.code_editor.see("insert")

        except Exception as e:
            print(f"Syntax highlighting error: {e}")

    def get_tag_for_token(self, token_type):
        """Get tag name for token type - SIMPLIFIED"""
        token_str = str(token_type)

        # Direct mapping based on token string
        if 'Keyword' in token_str:
            return 'keyword'
        elif 'String' in token_str or 'Literal.String' in token_str:
            return 'string'
        elif 'Comment' in token_str:
            return 'comment'
        elif 'Number' in token_str or 'Literal.Number' in token_str:
            return 'number'
        elif 'Name.Function' in token_str:
            return 'function'
        elif 'Name.Builtin' in token_str:
            return 'builtin'
        elif 'Name.Class' in token_str:
            return 'class'

        return None

    def update_editor_theme(self):
        """Editör arka plan ve renkleri güncelle"""
        theme_colors = self.get_theme_colors(self.current_theme)

        # Arka plan renklerini güncelle
        bg_color = self.hex_from_int(theme_colors['bg'])
        fg_color = self.hex_from_int(theme_colors['fg'])
        select_bg = theme_colors['select_bg']

        self.code_editor.configure(
            bg=bg_color,
            fg=fg_color,
            selectbackground=select_bg,
            insertbackground=fg_color
        )

    def on_theme_change(self, event=None):
        """Tema değiştiğinde çağrılır"""
        self.current_theme = self.theme_var.get()
        self.update_editor_theme()
        self.setup_syntax_tags()
        self.highlight_syntax()

    def on_language_change(self, event=None):
        """Dil değiştiğinde syntax highlighting'i güncelle"""
        self.highlight_syntax()

    def initialize_syntax_highlighting(self):
        """Syntax highlighting'i güvenli şekilde başlat"""
        try:
            self.setup_syntax_tags()
            self.update_editor_theme()
            self.highlight_syntax()
            print("✓ Syntax highlighting initialized")
        except Exception as e:
            print(f"Syntax highlighting initialization failed: {e}")
            self.syntax_enabled = False

    def on_text_change(self, event=None):
        """Text değiştiğinde syntax highlighting'i güncelle"""
        # Performans için biraz gecikme ekle
        if self.syntax_enabled:
            # Use debounced highlighting
            self._schedule_syntax_highlighting(delay=300)

        # Event'i print et debug için
        if event and hasattr(event, 'keysym'):
            print(f"Text change event: {event.keysym}")
        elif event:
            print(f"Text change event: {event}")

    def on_paste_change(self, event=None):
        """Paste sonrası syntax highlighting güncelle"""
        if self.syntax_enabled:
            # Force immediate syntax highlighting after paste
            # First, mark as modified to ensure check_for_changes picks it up
            self.code_editor.edit_modified(True)

            # Use debounced highlighting for better performance
            self._schedule_syntax_highlighting(delay=100)

        # Don't prevent default paste behavior
        return None

    def check_for_changes(self):
        """Text değişikliklerini sürekli kontrol et"""
        try:
            if self.code_editor.edit_modified():
                # Text değişti, highlighting yap
                if self.syntax_enabled:
                    self._schedule_syntax_highlighting(delay=200)
                # Reset the modified flag after processing
                self.code_editor.edit_modified(False)

            # Kendini tekrar çağır - reduced interval for better responsiveness
            self.root.after(150, self.check_for_changes)
        except:
            # GUI kapatılmış olabilir
            pass

    def _schedule_syntax_highlighting(self, delay=200):
        """Schedule syntax highlighting with debouncing"""
        # Cancel any existing timer
        if hasattr(self, 'highlighting_timer') and self.highlighting_timer:
            self.root.after_cancel(self.highlighting_timer)

        # Schedule new highlighting
        self.highlighting_timer = self.root.after(delay, self.highlight_syntax)

    def _apply_minimal_highlighting(self, code):
        """Apply minimal highlighting for large files"""
        # Clear all existing tags
        for tag_name in self.syntax_tags.values():
            self.code_editor.tag_remove(tag_name, '1.0', tk.END)

        # Use simple regex patterns for basic highlighting
        import re
        lines = code.split('\n')

        for line_no, line in enumerate(lines, 1):
            if not line.strip():
                continue

            # Highlight comments (anything after #)
            if '#' in line:
                comment_start = line.find('#')
                # Check if # is not inside a string
                before_hash = line[:comment_start]
                quote_count = before_hash.count('"') + before_hash.count("'")
                if quote_count % 2 == 0:  # Not inside string
                    start_pos = f"{line_no}.{comment_start}"
                    end_pos = f"{line_no}.{len(line)}"
                    self.code_editor.tag_add('comment', start_pos, end_pos)

            # Highlight keywords
            keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif',
                       'for', 'while', 'try', 'except', 'finally', 'with',
                       'return', 'yield', 'break', 'continue', 'pass',
                       'raise', 'assert', 'lambda', 'global', 'nonlocal']

            for keyword in keywords:
                pattern = r'\b' + keyword + r'\b'
                for match in re.finditer(pattern, line):
                    start = match.start()
                    end = match.end()
                    self.code_editor.tag_add('keyword', f"{line_no}.{start}", f"{line_no}.{end}")

            # Highlight strings (basic)
            # Single quotes
            for match in re.finditer(r"'[^']*'", line):
                start = match.start()
                end = match.end()
                self.code_editor.tag_add('string', f"{line_no}.{start}", f"{line_no}.{end}")

            # Double quotes
            for match in re.finditer(r'"[^"]*"', line):
                start = match.start()
                end = match.end()
                self.code_editor.tag_add('string', f"{line_no}.{start}", f"{line_no}.{end}")


def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = CodeAnimationStudioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()