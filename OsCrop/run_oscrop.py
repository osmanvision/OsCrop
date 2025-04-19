# test_run.py - OsCrop Test Utility
# Author: Os (Osman Vision)

import os
import subprocess

# === CONFIG ===
sample_folder = r"D:\OsCrop\samples"

scripts = {
    "1": {"name": "oscrop_full.py", "desc": "Full pipeline (remove BG + crop + resize)"},
    "2": {"name": "oscrop_bg_remover.py", "desc": "Background remover only"},
    "3": {"name": "oscrop_auto_alpha_crop.py", "desc": "Auto crop transparent PNGs"},
    "4": {"name": "oscrop_crop_detect.py", "desc": "Shape-based crop (non-transparent)"},
}

print("\n🧪 OsCrop Test Utility")
print("========================\n")
print("Available tools to test:")
for key, script in scripts.items():
    print(f" {key}. {script['desc']}")
print(" A. Test ALL scripts\n")

choice = input("Which tool would you like to test? (1/2/3/4/A): ").strip().upper()

if choice not in scripts and choice != "A":
    print("❌ Invalid choice. Exiting.")
    exit()

# === Inject input path dynamically ===
def run_script(script_name):
    print(f"\n▶️ Running {script_name}...")
    temp_code = f"_test_temp_{script_name}"

    with open(script_name, "r", encoding="utf-8") as original:
        lines = original.readlines()

    with open(temp_code, "w", encoding="utf-8") as temp:
        for line in lines:
            if line.strip().startswith("input_folder"):
                temp.write(f"input_folder = r\"{sample_folder}\"  # Injected for test\n")
            else:
                temp.write(line)

    try:
        subprocess.run(["python", temp_code], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
    finally:
        os.remove(temp_code)

# === Execute ===
if choice == "A":
    for key in scripts:
        run_script(scripts[key]["name"])
else:
    run_script(scripts[choice]["name"])

print("\n✅ Test run complete.")