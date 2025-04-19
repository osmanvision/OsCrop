"""
OsCrop v1.0 - Full Background Remover & Auto Cropper
Author: Os (Osman Vision)
License: Os Public License (v1.0)
Powered by OsCrop
"""

import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

# === 🔐 Tamper Check ===
LICENSE_KEY = "Author: Os"
if LICENSE_KEY not in __doc__:
    raise Exception("❌ Unauthorized version - license or author credit removed.")

# === 🛠 CONFIGURATION ===
input_folder = r"path\to\your\input_images"   # <- CHANGE THIS
output_folder = os.path.join(input_folder, "output_no_bg")
cropped_folder = os.path.join(output_folder, "output_crops")
output_size = 512
padding = 30
skipped_files = []

os.makedirs(output_folder, exist_ok=True)
os.makedirs(cropped_folder, exist_ok=True)

# === STEP 1: Background Removal ===
print("🔄 STEP 1: Removing backgrounds with rembg...")
for file in os.listdir(input_folder):
    if file.lower().endswith(".png"):
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)
        if not os.path.exists(out_path):
            with open(in_path, "rb") as inp:
                output = remove(inp.read())
            with open(out_path, "wb") as out:
                out.write(output)
            print(f"✅ BG Removed: {file}")
        else:
            print(f"⏩ Already exists (skipped): {file}")

# === STEP 2: Smart Crop + Resize ===
print("\n✂️ STEP 2: Cropping & Centering objects...")

object_count = 1
for file in os.listdir(output_folder):
    if not file.lower().endswith(".png"):
        continue

    path = os.path.join(output_folder, file)
    image_pil = Image.open(path).convert("RGBA")
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGBA2BGRA)

    alpha = image_cv[:, :, 3]
    _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"⚠️ No alpha-based object found in '{file}', skipping.")
        skipped_files.append(file)
        continue

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 100 or h < 100:
            continue

        x0 = max(0, x - padding)
        y0 = max(0, y - padding)
        x1 = min(image_pil.width, x + w + padding)
        y1 = min(image_pil.height, y + h + padding)

        cropped = image_pil.crop((x0, y0, x1, y1))

        if cropped.width <= output_size and cropped.height <= output_size:
            canvas = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
            offset_x = (output_size - cropped.width) // 2
            offset_y = (output_size - cropped.height) // 2
            canvas.paste(cropped, (offset_x, offset_y), cropped)
            final = canvas
        else:
            final = cropped

        save_path = os.path.join(cropped_folder, f"object_{object_count}.png")
        final.save(save_path)
        print(f"✅ object_{object_count}.png saved ({output_size}x{output_size})")

        object_count += 1

print(f"\n🎉 Done! Total objects saved: {object_count - 1}")
print("🔧 Powered by OsCrop")

# === END REPORT ===
if skipped_files:
    print("\n⚠️ The following files couldn't be processed using alpha-based cropping:")
    for f in skipped_files:
        print(f" - {f}")
    print("💡 Tip: Use oscrop_crop_detect.py to process these files using shape detection.\n")
