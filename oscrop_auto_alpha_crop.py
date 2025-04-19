"""
OsCrop v1.0 - Auto Alpha Cropper
Author: Os (Osman Vision)
License: Os Public License (v1.0)
🔧 Powered by OsCrop
"""

import os
import cv2
import numpy as np
from PIL import Image

# === CONFIGURATION ===
input_folder = r"D:\OsCrop\samples"   # <- CHANGE THIS
output_folder = os.path.join(input_folder, "alpha_crops")
output_size = 512
padding = 30
skipped_files = []

os.makedirs(output_folder, exist_ok=True)

print("\n✂️ Cropping transparent PNGs using alpha channel...\n")

object_count = 1
for file in os.listdir(input_folder):
    if not file.lower().endswith(".png"):
        continue

    path = os.path.join(input_folder, file)
    image_pil = Image.open(path)

    # ✅ Check for real alpha BEFORE converting
    if 'A' not in image_pil.getbands():
        print(f"⚠️ Skipped: '{file}' has no alpha channel (use oscrop_crop_detect.py instead)")
        skipped_files.append(file)
        continue

    # Now safe to convert
    image_pil = image_pil.convert("RGBA")
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

        save_path = os.path.join(output_folder, f"alpha_crop_{object_count}.png")
        final.save(save_path)
        print(f"✅ alpha_crop_{object_count}.png saved")
        object_count += 1


print(f"\n🎉 Done! Total objects saved: {object_count - 1}")
print("🔧 Powered by OsCrop")

if skipped_files:
    print("\n⚠️ The following files couldn't be cropped using alpha:")
    for f in skipped_files:
        print(f" - {f}")
    print("💡 Tip: Try oscrop_crop_detect.py if your images do not have transparency.")
