"""
OsCrop v1.0 - Background Remover Only
Author: Os (Osman Vision)
License: Os Public License (v1.0)
🔧 Powered by OsCrop
"""

import os
from rembg import remove

# === 🔐 Tamper Check ===
LICENSE_KEY = "Author: Os"
if LICENSE_KEY not in __doc__:
    raise Exception("❌ Unauthorized version - license or author credit removed.")

# === 🛠 CONFIGURATION ===
input_folder = r"path\\to\\your\\input_images"  # <- CHANGE THIS
output_folder = os.path.join(input_folder, "output_no_bg")
overwrite_existing = False  # Set to True if you want to reprocess existing files

supported_exts = [".png", ".jpg", ".jpeg", ".webp"]
skipped_files = []
processed_count = 0

os.makedirs(output_folder, exist_ok=True)

print("\n🔄 Removing backgrounds using rembg...\n")

for file in os.listdir(input_folder):
    if not any(file.lower().endswith(ext) for ext in supported_exts):
        continue

    in_path = os.path.join(input_folder, file)
    out_path = os.path.join(output_folder, file)

    if not overwrite_existing and os.path.exists(out_path):
        print(f"⏩ Skipped (already exists): {file}")
        skipped_files.append(file)
        continue

    with open(in_path, "rb") as inp:
        output_bytes = remove(inp.read())
    with open(out_path, "wb") as out:
        out.write(output_bytes)

    print(f"✅ Background removed: {file}")
    processed_count += 1

print(f"\n🎉 Done! Total backgrounds removed: {processed_count}")
print("🔧 Powered by OsCrop")

if skipped_files:
    print(f"\n⚠️ Skipped {len(skipped_files)} already-processed files:")
    for f in skipped_files:
        print(f" - {f}")
    print("💡 Tip: Set `overwrite_existing = True` if you want to regenerate these.\n")
