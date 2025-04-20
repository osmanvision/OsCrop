[![OsCrop banner](https://github.com/osmanvision/OsCrop/blob/main/oscrop_banner.png)](https://github.com/osmanvision/OsCrop)

# 🖼️ OsCrop

**OsCrop** is a simple yet powerful open-source tool for:

- 🧼 Removing backgrounds from images (PNG, JPG, WEBP)
- ✂️ Automatically cropping the main object
- 🎯 Outputting clean 512x512 images centered on transparent backgrounds

Made for creators and developers who want fast, clean asset extraction — perfect for Telegram stickers, digital design, AI datasets, and more.

---

📸 Use Cases

Whether you're a creator, developer, or just someone working with digital visuals — OsCrop simplifies your workflow.

- 🧩 Creating Telegram, WhatsApp, or Discord stickers
- 🛍️ Cleaning up product images for online shops
- 🧠 Preparing consistent assets for machine learning datasets
- 🎨 Extracting and isolating emoji, clipart, avatars, or sprites
- 📚 Streamlining bulk image cleanup for digital archives or design packs

---

## ✨ Features

- 🔍 Detects objects using alpha transparency or shape detection
- 🧼 Cleans up black glow or leftover outlines
- 🪄 Automatically centers and resizes objects onto transparent 512x512 canvases
- 🧠 Skips previously processed images
- 🔁 Full automation pipeline (removal + cropping)
- 🧰 Supports PNG, JPG, and WEBP
- 🔐 Includes author license check with anti-tamper

---

## 📁 Folder Structure

```
OsCrop/
├── oscrop_full.py               # Full pipeline: background removal + crop + resize
├── oscrop_bg_remover.py        # Only removes background using rembg
├── oscrop_auto_alpha_crop.py   # Auto-crops transparent PNGs using alpha mask
├── oscrop_crop_detect.py       # Crops non-transparent PNG/JPG/WEBP using object detection
├── run_oscrop.py               # Easy launcher script for non-developers
├── LICENSE                     # Os Public License v1.0
├── README.md                   # You're reading it
├── requirements.txt            # Python dependencies
└── samples/                    # Includes sample images for testing
```

---

## 📦 Installation

Make sure you have **Python 3.8 or higher** installed.

```bash
pip install rembg opencv-python pillow numpy
```

✅ Python 3.8 or higher recommended\
❌ No GPU required\
💻 Works on Windows, Mac, Linux (tested)

---

## ⚙️ How to Use

### 1. Easy Launcher (Recommended for non-devs)

```bash
python run_oscrop.py
```
This will show a menu to choose:
1. Full Process
2. Background Only
3. Crop Transparent PNGs
4. Crop Non-Transparent Images

You’ll be asked to set or confirm your `input_folder`.

---

### 2. Full Manual Scripts

> Make sure to set `input_folder` in each script before running.

#### A. Full Pipeline
```bash
python oscrop_full.py
```
Creates `output_no_bg/output_crops/`

#### B. Just Remove Background
```bash
python oscrop_bg_remover.py
```
Creates `output_no_bg/`

#### C. Only Crop Transparent PNGs
```bash
python oscrop_auto_alpha_crop.py
```
Creates `alpha_crops/` folder

#### D. Crop Non-Transparent Images
```bash
python oscrop_crop_detect.py
```
Creates `shape_crops/` folder

> 🔄 If `oscrop_auto_alpha_crop.py` detects no alpha channel, it will skip and suggest using `oscrop_crop_detect.py`.
> 🧠 `oscrop_crop_detect.py` also skips full-sheet crops intelligently if they cover the whole image.

---

## 🧪 Output Samples

- All cropped images are **centered** and **padded** into clean `512x512` boxes
- Output folders like `alpha_crops`, `shape_crops`, `output_crops` are created automatically
- Files are named sequentially like `alpha_crop_1.png`, `detect_crop_3.png`, etc

### 📂 Sample Images
Included in the `samples/` folder:
- `dark_bg.png` – Object sheet with dark background
- `white_bg.png` – Object sheet with white background
- `transparent_sheet.png` – PNG with alpha background

You can test the tools on these to see how they behave in different scenarios.

---

## 📄 License

```
Os Public License v1.0
Copyright (c) 2025 Os (Osman Vision)

You are free to use, modify, and distribute the code,
BUT the author credit must remain visible.

Tampering with the license block or removing author lines
may result in broken functionality.

For commercial licensing, contact: heyosmanvision@gmail.com
```

---

## 📬 Contact

**Instagram**: [@osman\_vision](https://www.instagram.com/osman_vision)\
**Email**: [heyosmanvision@gmail.com](mailto:heyosmanvision@gmail.com)
- Discord: osman_vision
  
### 📬 Get in Touch

- Instagram: [@osman_vision](https://www.instagram.com/osman_vision)
- Email: heyosmanvision@gmail.com
- Discord: osman_vision


---

🔧 Powered by **OsCrop** by Osman Vision
