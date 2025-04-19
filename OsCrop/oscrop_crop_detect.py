"""
OsCrop v1.0 - Object Cropper for Normal Images (No Transparency Needed)
Author: Os (Osman Vision)
License: Os Public License (v1.0)
🔧 Powered by OsCrop
"""

import os
import cv2
from PIL import Image
import numpy as np

# === 🔐 Tamper Check ===
LICENSE_KEY = "Author: Os"
if LICENSE_KEY not in __doc__:
    raise Exception("❌ Unauthorized version - license or author credit removed.")

# === 🛠 CONFIGURATION ===
input_folder = r"D:\OsCrop\samples\white_bg"  # <- CHANGE THIS TO dark_bg or white_bg
output_folder = os.path.join(input_folder, "shape_crops")
output_size = 512
padding = 30
supported_exts = [".png", ".jpg", ".jpeg", ".webp"]
skipped_files = []

os.makedirs(output_folder, exist_ok=True)

print("\n✂️ Detecting and cropping objects from non-transparent images...\n")

object_count = 1
for file in os.listdir(input_folder):
    if not any(file.lower().endswith(ext) for ext in supported_exts):
        continue

    path = os.path.join(input_folder, file)
    image = cv2.imread(path)

    if image is None:
        print(f"❌ Could not open file: {file}")
        skipped_files.append(file)
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding helps detect on varied lighting/backgrounds
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 5)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"⚠️ No object detected in '{file}', skipping.")
        skipped_files.append(file)
        continue

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Skip small noise
        if w < 100 or h < 100:
            continue

        # Avoid full image crop — only if no other contours remain
        img_h, img_w = image.shape[:2]
        if w > img_w * 0.95 and h > img_h * 0.95 and len(contours) == 1:
            print(f"⚠️ Skipped full image bounding box in '{file}'")
            continue

        x0 = max(0, x - padding)
        y0 = max(0, y - padding)
        x1 = min(image.shape[1], x + w + padding)
        y1 = min(image.shape[0], y + h + padding)

        cropped = image[y0:y1, x0:x1]
        pil_img = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGBA))

        if pil_img.width <= output_size and pil_img.height <= output_size:
            canvas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
            offset_x = (output_size - pil_img.width) // 2
            offset_y = (output_size - pil_img.height) // 2
            canvas.paste(pil_img, (offset_x, offset_y))
            final = canvas
        else:
            final = pil_img

        save_path = os.path.join(output_folder, f"detect_crop_{object_count}.png")
        final.save(save_path)
        print(f"✅ detect_crop_{object_count}.png saved")

        object_count += 1

print(f"\n🎉 Done! Total objects saved: {object_count - 1}")
print("🔧 Powered by OsCrop")

if skipped_files:
    print("\n⚠️ The following files couldn't be processed:")
    for f in skipped_files:
        print(f" - {f}")
    print("💡 Tip: Make sure they contain visible shapes or try oscrop_auto_alpha_crop.py for PNGs with transparency.")
