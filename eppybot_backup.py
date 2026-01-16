"""
EppyBot - Professional Image Enhancement Suite
A sleek, modern desktop application for enhancing images to ultra-high-quality 4K UHD resolution
with advanced AI-inspired processing techniques and professional-grade controls.

Requirements: pip install pillow
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Dict, List
from PIL import Image, ImageFilter, ImageEnhance
from PIL import ImageTk
import threading
from datetime import datetime


class ImageEnhancerApp:
    """
    Professional Image Enhancement Suite with modern UI and advanced features.
    """
    
    # Modern Black & White Color Scheme
    COLORS = {
        'bg_dark': '#0a0a0a',           # Deep black background
        'bg_medium': '#1a1a1a',         # Medium black
        'bg_light': '#2a2a2a',          # Light black/dark gray
        'accent': '#ffffff',            # Pure white
        'accent_hover': '#e0e0e0',      # Light gray
        'text_primary': '#ffffff',      # White text
        'text_secondary': '#a0a0a0',    # Gray text
        'text_muted': '#606060',        # Muted gray
        'border': '#3a3a3a',            # Border color
        'success': '#ffffff',           # White for success
        'warning': '#d0d0d0',           # Light gray for warnings
    }
    
    # Enhancement Presets
    PRESETS = {
        'Natural': {
            'upscale_factor': 3.0,
            'sharpen_strength': 1.3,
            'contrast': 1.05,
            'color_saturation': 1.0,
            'brightness': 1.0
        },
        'Vivid': {
            'upscale_factor': 3.0,
            'sharpen_strength': 1.6,
            'contrast': 1.15,
            'color_saturation': 1.2,
            'brightness': 1.05
        },
        'Portrait': {
            'upscale_factor': 2.5,
            'sharpen_strength': 1.2,
            'contrast': 1.08,
            'color_saturation': 1.05,
            'brightness': 1.08
        },
        'Landscape': {
            'upscale_factor': 3.5,
            'sharpen_strength': 1.7,
            'contrast': 1.12,
            'color_saturation': 1.15,
            'brightness': 1.02
        },
        'Professional': {
            'upscale_factor': 4.0,
            'sharpen_strength': 1.5,
            'contrast': 1.10,
            'color_saturation': 1.08,
            'brightness': 1.05
        }
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("EppyBot - Professional Image Enhancement Suite")
        self.root.geometry("1600x950")
        self.root.resizable(True, True)
        
        # Set dark theme
        self.root.configure(bg=self.COLORS['bg_dark'])
        
        # Application state
        self.original_image: Optional[Image.Image] = None
        self.enhanced_image: Optional[Image.Image] = None
        self.input_path: Optional[str] = None
        self.is_processing = False
        self.batch_mode = False
        self.batch_files: List[str] = []
        self.current_preset = 'Natural'
        
        # Target 4K UHD resolution
        self.TARGET_WIDTH = 3840
        self.TARGET_HEIGHT = 2160
        
        # Setup modern UI
        self._setup_modern_ui()
        
        
    def _setup_modern_ui(self):
        """Initialize the modern black & white user interface."""
        
        # Configure root grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Modern Header Frame
        header_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'], height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.COLORS['bg_dark'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        title_label = tk.Label(
            header_content,
            text="EPPYBOT",
            font=("Helvetica", 28, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_content,
            text="Professional Image Enhancement Suite",
            font=("Helvetica", 10),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['text_secondary'],
            anchor="w"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Version badge
        version_label = tk.Label(
            header_content,
            text="v2.0",
            font=("Helvetica", 9, "bold"),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_secondary'],
            padx=8,
            pady=3
        )
        version_label.pack(side=tk.RIGHT)
        
        # Main content frame with modern styling
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        main_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        
        # Left Panel - Controls
        self._create_modern_control_panel(main_frame)
        
        # Right Panel - Image Display
        self._create_modern_display_panel(main_frame)
        
        # Modern Status bar
        self.status_var = tk.StringVar(value="Ready • Upload an image to begin")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=0,
            relief=tk.FLAT,
            anchor=tk.W,
            font=("Helvetica", 9),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_secondary'],
            padx=30,
            pady=12
        )
        status_bar.grid(row=2, column=0, sticky="ew")
        
        
    def _create_modern_control_panel(self, parent):
        """Create the modern control panel with black & white theme."""
        
        # Main container frame
        container_frame = tk.Frame(parent, bg=self.COLORS['bg_medium'], relief=tk.FLAT, bd=0)
        container_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10))
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas with modern scrollbar
        canvas = tk.Canvas(container_frame, bg=self.COLORS['bg_medium'], highlightthickness=0)
        
        # Custom styled scrollbar
        scrollbar_frame = tk.Frame(container_frame, bg=self.COLORS['bg_dark'], width=8)
        scrollbar = tk.Canvas(scrollbar_frame, bg=self.COLORS['bg_light'], width=4, highlightthickness=0)
        
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS['bg_medium'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Simple scrollbar setup
        def on_canvas_scroll(*args):
            canvas.yview(*args)
        
        canvas.configure(yscrollcommand=lambda *args: None)
        
        # Pack canvas
        canvas.grid(row=0, column=0, sticky="nsew")
        
        # Configure scrollable_frame
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # === UPLOAD SECTION ===
        self._create_section_header(scrollable_frame, 0, "UPLOAD")
        
        upload_btn = self._create_modern_button(
            scrollable_frame,
            text="SELECT IMAGE",
            command=self._upload_image,
            row=1,
            style='primary'
        )
        
        # Batch mode toggle
        batch_frame = tk.Frame(scrollable_frame, bg=self.COLORS['bg_medium'])
        batch_frame.grid(row=2, column=0, pady=(10, 0), padx=20, sticky="ew")
        
        self.batch_var = tk.BooleanVar(value=False)
        batch_check = tk.Checkbutton(
            batch_frame,
            text="Batch Mode (Multiple Files)",
            variable=self.batch_var,
            font=("Helvetica", 9),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_secondary'],
            selectcolor=self.COLORS['bg_dark'],
            activebackground=self.COLORS['bg_medium'],
            activeforeground=self.COLORS['text_primary'],
            cursor="hand2",
            command=self._toggle_batch_mode
        )
        batch_check.pack(anchor="w")
        
        self.filename_label = tk.Label(
            scrollable_frame,
            text="No file selected",
            font=("Helvetica", 9),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_muted'],
            wraplength=320,
            justify=tk.LEFT
        )
        self.filename_label.grid(row=3, column=0, pady=(8, 0), padx=20, sticky="w")
        
        # Image info display
        self.info_label = tk.Label(
            scrollable_frame,
            text="",
            font=("Helvetica", 8),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text_muted'],
            wraplength=320,
            justify=tk.LEFT
        )
        self.info_label.grid(row=4, column=0, pady=(5, 15), padx=20, sticky="w")
        
        self._create_separator(scrollable_frame, 5)
        
        # === PRESETS SECTION ===
        self._create_section_header(scrollable_frame, 6, "ENHANCEMENT PRESETS")
        
        preset_frame = tk.Frame(scrollable_frame, bg=self.COLORS['bg_medium'])
        preset_frame.grid(row=7, column=0, pady=(0, 15), padx=20, sticky="ew")
        preset_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.preset_var = tk.StringVar(value='Natural')
        
        presets = ['Natural', 'Vivid', 'Portrait', 'Landscape', 'Professional']
        for idx, preset in enumerate(presets):
            row = idx // 3
            col = idx % 3
            
            preset_btn = tk.Radiobutton(
                preset_frame,
                text=preset,
                variable=self.preset_var,
                value=preset,
                font=("Helvetica", 9, "bold"),
                bg=self.COLORS['bg_light'],
                fg=self.COLORS['text_primary'],
                selectcolor=self.COLORS['bg_dark'],
                activebackground=self.COLORS['bg_light'],
                activeforeground=self.COLORS['accent'],
                cursor="hand2",
                indicatoron=False,
                width=10,
                pady=8,
                command=self._apply_preset
            )
            preset_btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
        
        self._create_separator(scrollable_frame, 8)
        
        # === OUTPUT FORMAT SECTION ===
        self._create_section_header(scrollable_frame, 9, "OUTPUT FORMAT")
        
        self.format_var = tk.StringVar(value="PNG")
        
        format_frame = tk.Frame(scrollable_frame, bg=self.COLORS['bg_medium'])
        format_frame.grid(row=10, column=0, padx=20, pady=(0, 15), sticky="ew")
        format_frame.grid_columnconfigure((0, 1), weight=1)
        
        png_radio = tk.Radiobutton(
            format_frame,
            text="PNG (Lossless)",
            variable=self.format_var,
            value="PNG",
            font=("Helvetica", 9),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_primary'],
            selectcolor=self.COLORS['bg_dark'],
            activebackground=self.COLORS['bg_light'],
            activeforeground=self.COLORS['accent'],
            cursor="hand2",
            indicatoron=False,
            pady=8
        )
        png_radio.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        jpg_radio = tk.Radiobutton(
            format_frame,
            text="JPG (Optimized)",
            variable=self.format_var,
            value="JPG",
            font=("Helvetica", 9),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_primary'],
            selectcolor=self.COLORS['bg_dark'],
            activebackground=self.COLORS['bg_light'],
            activeforeground=self.COLORS['accent'],
            cursor="hand2",
            indicatoron=False,
            pady=8
        )
        jpg_radio.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        self._create_separator(scrollable_frame, 11)
        
        # === MANUAL CONTROLS SECTION ===
        self._create_section_header(scrollable_frame, 12, "MANUAL CONTROLS")
        
        # Upscale Factor
        self._create_modern_slider(
            scrollable_frame, 13,
            "Upscale Factor",
            2.0, 4.0, 3.0, 0.1
        )
        
        # Sharpen Strength
        self._create_modern_slider(
            scrollable_frame, 14,
            "Sharpen",
            1.0, 2.0, 1.5, 0.1
        )
        
        # Contrast
        self._create_modern_slider(
            scrollable_frame, 15,
            "Contrast",
            0.8, 1.5, 1.10, 0.01
        )
        
        # Color Saturation
        self._create_modern_slider(
            scrollable_frame, 16,
            "Saturation",
            0.8, 1.5, 1.08, 0.01
        )
        
        # Brightness
        self._create_modern_slider(
            scrollable_frame, 17,
            "Brightness",
            0.9, 1.2, 1.05, 0.01
        )
        
        self._create_separator(scrollable_frame, 18)
        
        # === ACTION BUTTONS ===
        self._create_section_header(scrollable_frame, 19, "ACTIONS")
        
        # Enhance Button
        enhance_btn = self._create_modern_button(
            scrollable_frame,
            text="ENHANCE IMAGE",
            command=self._enhance_image,
            row=20,
            style='accent'
        )
        
        # Save Button
        save_btn = self._create_modern_button(
            scrollable_frame,
            text="SAVE / EXPORT",
            command=self._save_image,
            row=21,
            style='secondary'
        )
        
        # Reset Button
        reset_btn = self._create_modern_button(
            scrollable_frame,
            text="RESET ALL",
            command=self._reset_all,
            row=22,
            style='outline'
        )
        
        # Add spacing at bottom
        bottom_spacer = tk.Frame(scrollable_frame, bg=self.COLORS['bg_medium'], height=30)
        bottom_spacer.grid(row=23, column=0)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def _create_slider(self, parent, row, label_text, from_, to, default, resolution, info_text):
        """Create a labeled slider with info text."""
        
        # Container frame
        slider_frame = tk.Frame(parent, bg="white")
        slider_frame.grid(row=row, column=0, pady=8, padx=15, sticky="ew")
        slider_frame.grid_columnconfigure(0, weight=1)
        
        # Label and value display
        header_frame = tk.Frame(slider_frame, bg="white")
        header_frame.grid(row=0, column=0, sticky="ew")
        
        label = tk.Label(
            header_frame,
            text=label_text,
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        label.pack(side=tk.LEFT)
        
        value_var = tk.DoubleVar(value=default)
        value_label = tk.Label(
            header_frame,
            textvariable=value_var,
            font=("Helvetica", 10),
            bg="white",
            fg="#3498db"
        )
        value_label.pack(side=tk.RIGHT)
        
        # Slider
        slider = tk.Scale(
            slider_frame,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            variable=value_var,
            showvalue=0,
            bg="white",
            highlightthickness=0,
            troughcolor="#bdc3c7",
            cursor="hand2"
        )
        slider.grid(row=1, column=0, sticky="ew")
        
        # Info text
        info = tk.Label(
            slider_frame,
            text=info_text,
            font=("Helvetica", 8),
            bg="white",
            fg="#95a5a6",
            wraplength=280,
            justify=tk.LEFT
        )
        info.grid(row=2, column=0, sticky="w")
        
        # Store variable for later access
        setattr(self, f"{label_text.lower().replace(' ', '_')}_var", value_var)
        
    def _create_display_panel(self, parent):
        """Create the right display panel for showing images."""
        
        display_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        display_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(
            display_frame,
            text="📊 Image Comparison",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=15)
        
        # Original Image Panel
        original_frame = tk.LabelFrame(
            display_frame,
            text="Original Image",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        original_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.original_canvas = tk.Canvas(
            original_frame,
            bg="#ecf0f1",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Enhanced Image Panel
        enhanced_frame = tk.LabelFrame(
            display_frame,
            text="Enhanced Image",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#34495e",
            relief=tk.GROOVE,
            bd=2
        )
        enhanced_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self.enhanced_canvas = tk.Canvas(
            enhanced_frame,
            bg="#ecf0f1",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        self.enhanced_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info panel
        info_frame = tk.Frame(display_frame, bg="white")
        info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        info_text = tk.Label(
            info_frame,
            text="💡 Tips: Start with images at least 800×600 | Adjust sharpening carefully | "
                 "PNG for graphics, JPG for photos",
            font=("Helvetica", 9),
            bg="white",
            fg="#7f8c8d",
            wraplength=900,
            justify=tk.CENTER
        )
        info_text.pack()
        
    def _upload_image(self):
        """Handle image upload."""
        
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Load the image
            self.original_image = Image.open(file_path)
            if self.original_image.mode != 'RGB':
                self.original_image = self.original_image.convert('RGB')
            
            self.input_path = file_path
            
            # Check image size constraints
            width, height = self.original_image.size
            
            if width > 8000 or height > 8000:
                messagebox.showerror(
                    "Image Too Large",
                    f"Image too large! Maximum dimension is 8000px.\n"
                    f"Your image: {width}×{height}"
                )
                return
            
            if width < 100 or height < 100:
                messagebox.showerror(
                    "Image Too Small",
                    f"Image too small! Minimum dimension is 100px.\n"
                    f"Your image: {width}×{height}"
                )
                return
            
            # Update filename label
            filename = os.path.basename(file_path)
            self.filename_label.config(
                text=f"File: {filename}\nSize: {width}×{height}",
                fg="#27ae60"
            )
            
            # Display original image
            self._display_image(self.original_image, self.original_canvas)
            
            # Clear enhanced image
            self.enhanced_image = None
            self.enhanced_canvas.delete("all")
            
            self.status_var.set(f"Image loaded: {filename} ({width}×{height})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            self.status_var.set("Error loading image")
            
    def _display_image(self, image: Image.Image, canvas: tk.Canvas):
        """Display an image on a canvas, scaled to fit."""
        
        canvas.delete("all")
        
        # Get canvas dimensions
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 500
            canvas_height = 400
        
        # Calculate scaling to fit canvas
        img_width, img_height = image.size
        scale = min(canvas_width / img_width, canvas_height / img_height) * 0.95
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize for display
        display_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        
        # Store reference to prevent garbage collection
        canvas.image = photo
        
        # Display centered
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
    def _enhance_image(self):
        """Handle image enhancement in a separate thread."""
        
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please upload an image first!")
            return
        
        if self.is_processing:
            messagebox.showinfo("Processing", "Enhancement is already in progress!")
            return
        
        # Run enhancement in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._perform_enhancement, daemon=True)
        thread.start()
        
    def _perform_enhancement(self):
        """Perform the actual image enhancement."""
        
        self.is_processing = True
        self.status_var.set("Enhancing image... Please wait...")
        
        try:
            # Get parameter values
            upscale_factor = self.upscale_factor_var.get()
            sharpen = self.sharpen_strength_var.get()
            contrast = self.contrast_var.get()
            color = self.color_saturation_var.get()
            brightness = self.brightness_var.get()
            
            image = self.original_image.copy()
            
            # Get original dimensions
            orig_width, orig_height = image.size
            aspect_ratio = orig_width / orig_height
            
            # Calculate initial upscale dimensions
            new_width = int(orig_width * upscale_factor)
            new_height = int(orig_height * upscale_factor)
            
            # Step 1: Multi-step intelligent upscaling to ~4K
            self.status_var.set(f"Upscaling from {orig_width}×{orig_height} to {new_width}×{new_height}...")
            img_upscaled = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Step 2: Fit to 4K bounds while preserving aspect ratio
            if new_width > self.TARGET_WIDTH or new_height > self.TARGET_HEIGHT:
                width_scale = self.TARGET_WIDTH / new_width
                height_scale = self.TARGET_HEIGHT / new_height
                scale = min(width_scale, height_scale)
                
                final_width = int(new_width * scale)
                final_height = int(new_height * scale)
                
                self.status_var.set(f"Fitting to 4K: {final_width}×{final_height}...")
                img_upscaled = img_upscaled.resize((final_width, final_height), Image.LANCZOS)
            else:
                # If under 4K, try to get closer to 4K if possible
                if aspect_ratio >= 1:  # Landscape or square
                    if new_width < self.TARGET_WIDTH:
                        scale = min(self.TARGET_WIDTH / new_width, 1.5)
                        final_width = int(new_width * scale)
                        final_height = int(new_height * scale)
                        img_upscaled = img_upscaled.resize((final_width, final_height), Image.LANCZOS)
                else:  # Portrait
                    if new_height < self.TARGET_HEIGHT:
                        scale = min(self.TARGET_HEIGHT / new_height, 1.5)
                        final_width = int(new_width * scale)
                        final_height = int(new_height * scale)
                        img_upscaled = img_upscaled.resize((final_width, final_height), Image.LANCZOS)
            
            # Step 3: Advanced denoising pipeline
            self.status_var.set("Applying advanced denoising...")
            img_denoised = img_upscaled.filter(ImageFilter.GaussianBlur(radius=1.0))
            img_denoised = img_denoised.filter(ImageFilter.MedianFilter(size=3))
            
            # Step 4: Detail recovery with UnsharpMask
            self.status_var.set("Recovering details with unsharp mask...")
            unsharp_radius = 1.5 + (sharpen - 1.0)
            unsharp_percent = int(100 + (sharpen * 60))
            unsharp_threshold = 3
            
            img_detailed = img_denoised.filter(
                ImageFilter.UnsharpMask(
                    radius=unsharp_radius,
                    percent=unsharp_percent,
                    threshold=unsharp_threshold
                )
            )
            
            # Step 5: Brightness enhancement
            self.status_var.set("Enhancing brightness...")
            brightness_enhancer = ImageEnhance.Brightness(img_detailed)
            img_bright = brightness_enhancer.enhance(brightness)
            
            # Step 6: Contrast enhancement
            self.status_var.set("Enhancing contrast...")
            contrast_enhancer = ImageEnhance.Contrast(img_bright)
            img_contrast = contrast_enhancer.enhance(contrast)
            
            # Step 7: Color saturation enhancement
            self.status_var.set("Enhancing color saturation...")
            color_enhancer = ImageEnhance.Color(img_contrast)
            img_color = color_enhancer.enhance(color)
            
            # Step 8: Final mild sharpening pass
            self.status_var.set("Applying final sharpening...")
            img_final = img_color.filter(
                ImageFilter.UnsharpMask(
                    radius=1.2,
                    percent=110,
                    threshold=2
                )
            )
            
            # Store enhanced image
            self.enhanced_image = img_final
            
            # Display enhanced image on UI thread
            self.root.after(0, self._display_image, self.enhanced_image, self.enhanced_canvas)
            
            final_width, final_height = self.enhanced_image.size
            self.status_var.set(
                f"Enhancement complete! Final size: {final_width}×{final_height}"
            )
            
            # Show success message
            self.root.after(
                0,
                messagebox.showinfo,
                "Success",
                f"Image enhanced successfully!\n\n"
                f"Original: {orig_width}×{orig_height}\n"
                f"Enhanced: {final_width}×{final_height}"
            )
            
        except Exception as e:
            self.root.after(
                0,
                messagebox.showerror,
                "Enhancement Error",
                f"Failed to enhance image:\n{str(e)}"
            )
            self.status_var.set("Enhancement failed")
        finally:
            self.is_processing = False
            
    def _save_image(self):
        """Save the enhanced image."""
        
        if self.enhanced_image is None:
            messagebox.showwarning("No Enhanced Image", "Please enhance an image first!")
            return
        
        output_format = self.format_var.get()
        
        # Determine file extension and filter
        if output_format == "PNG":
            default_ext = ".png"
            filetypes = [("PNG files", "*.png"), ("All files", "*.*")]
        else:
            default_ext = ".jpg"
            filetypes = [("JPEG files", "*.jpg *.jpeg"), ("All files", "*.*")]
        
        # Generate default filename
        if self.input_path:
            base_name = os.path.splitext(os.path.basename(self.input_path))[0]
            default_name = f"{base_name}_eppybot_enhanced{default_ext}"
        else:
            default_name = f"eppybot_enhanced{default_ext}"
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            title="Save Enhanced Image",
            defaultextension=default_ext,
            initialfile=default_name,
            filetypes=filetypes
        )
        
        if not save_path:
            return
        
        try:
            # Save the image
            if output_format == "PNG":
                self.enhanced_image.save(save_path, 'PNG', quality=100, optimize=False)
            else:
                # Ensure RGB mode for JPEG
                if self.enhanced_image.mode in ('RGBA', 'LA', 'P'):
                    img_to_save = self.enhanced_image.convert('RGB')
                else:
                    img_to_save = self.enhanced_image
                img_to_save.save(save_path, 'JPEG', quality=95, optimize=True, subsampling=0)
            
            self.status_var.set(f"Image saved: {os.path.basename(save_path)}")
            messagebox.showinfo(
                "Success",
                f"Enhanced image saved successfully!\n\n{save_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")
            self.status_var.set("Failed to save image")


def main():
    """Main application entry point."""
    
    root = tk.Tk()
    
    # Set application icon (optional - will fail gracefully if no icon)
    try:
        # You can add an icon file if desired
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Create and run the application
    app = ImageEnhancerApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()