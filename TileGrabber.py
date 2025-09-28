import os
import json
import requests
from PIL import Image

# -------------------------
# Load config
# -------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

# Save folder
save_folder = os.path.abspath(config.get("tiles_save_folder", "./images"))
os.makedirs(save_folder, exist_ok=True)

# Ranges
first_start = config.get("start_tile_x", 110)
first_end = config.get("end_tile_x", 147)
second_start = config.get("start_tile_y", 887)
second_end = config.get("end_tile_y", 918)

# Placeholder settings
placeholder_cfg = config.get("placeholder", {})
placeholder_type = placeholder_cfg.get("type", "transparent").lower()  # "solid" or "transparent"
fill_color = None
if placeholder_type == "solid":
    hex_color = placeholder_cfg.get("color", "#EC407A").lstrip("#")
    fill_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
# Transparency replacement settings
replace_cfg = config.get("replace_transparency", {})
replace_type = replace_cfg.get("type", "keep").lower()  # "solid" to replace, "keep" to leave transparency
replacement_color = None
if replace_type == "solid":
    hex_replace = replace_cfg.get("color", "#808080").lstrip("#")
    replacement_color = tuple(int(hex_replace[i:i+2], 16) for i in (0, 2, 4)) + (255,)
    
# -------------------------
# Download loop
# -------------------------
saved_files = []  # Keep track of saved images

for first in range(first_start, first_end + 1):
    for second in range(second_start, second_end + 1):
        url = f"https://backend.wplace.live/files/s0/tiles/{first}/{second}.png"
        filename = os.path.join(save_folder, f"{first}_{second}.png")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {url} → {filename}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Create placeholder
                if placeholder_type == "solid":
                    img = Image.new("RGB", (1000, 1000), fill_color)
                else:
                    img = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
                img.save(filename, format="PNG")
                print(f"Image not found, created placeholder: {filename}")
            else:
                print(f"Failed {url}: {e}")
                continue
        except Exception as e:
            print(f"Failed {url}: {e}")
            continue

        saved_files.append(filename)

# -------------------------
# Replace transparent pixels if enabled
# -------------------------
if replacement_color:
    print("Replacing transparent pixels in all saved images...")
    for filename in saved_files:
        img = Image.open(filename).convert("RGBA")
        pixels = img.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    pixels[x, y] = replacement_color
        img.save(filename, format="PNG")
    print("Finished replacing transparent pixels.")
