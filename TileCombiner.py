from PIL import Image
from tqdm import tqdm
import threading
import time
import os
import json

# Load config
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

# Resolve paths relative to script location
images_folder = os.path.abspath(os.path.join(script_dir, config.get("tiles_save_folder", "./images")))
output_folder = os.path.abspath(os.path.join(script_dir, config.get("combined_save_folder", "./combined")))
prompt_continue = config.get("prompt_continue_after_estimate", True)

# Ensure input folder exists
if not os.path.isdir(images_folder):
    print(f"Folder not found: {images_folder}")
    exit()

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

print(f"Using images folder: {images_folder}")
print(f"Using output folder: {output_folder}")

def get_safe_filename(folder, base_name="stitched", ext=".png", start_counter=2):
    """
    Return a non-colliding filepath in `folder`.
    - If "stitched.png" doesn't exist -> return that.
    - Otherwise try stitched_0002.png, stitched_0003.png, ...
    `start_counter` controls the first suffix (default=2 -> _0002).
    """
    # Ensure folder exists
    os.makedirs(folder, exist_ok=True)

    # Normalize extension
    if not ext.startswith("."):
        ext = "." + ext

    # Try the base filename first (stitched.png)
    first_path = os.path.join(folder, f"{base_name}{ext}")
    if not os.path.exists(first_path):
        return first_path

    # Otherwise start at the requested counter (0002 by default)
    counter = start_counter
    while True:
        candidate = os.path.join(folder, f"{base_name}_{counter:04d}{ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

folder = os.path.join(script_dir, "images")

# Ensure input folder exists
if not os.path.isdir(folder):
    print(f"Folder not found: {folder}")
    exit()


# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read all PNG files (case-insensitive)
files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
if not files:
    print("No PNG files found in the folder.")
    exit()
    
# First, extract all grid coordinates
coords = []
for f in files:
    try:
        x_str, y_str = f.replace(".png","").split("_")
        x_grid, y_grid = int(x_str), int(y_str)
        coords.append((x_grid, y_grid))
    except Exception as e:
        print(f"Skipping {f}: {e}")
# Find minimum X and Y to normalize coordinates
min_x = min(x for x, y in coords)
min_y = min(y for x, y in coords)

# Now load images and apply normalized coordinates
images = []
TILE_SIZE = 1000

for f in tqdm(files, desc="Loading images", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}]"):
    try:
        x_str, y_str = f.replace(".png","").split("_")
        x_grid, y_grid = int(x_str), int(y_str)

        # Normalize coordinates so top-left tile is at (0,0)
        x = (x_grid - min_x) * TILE_SIZE
        y = (y_grid - min_y) * TILE_SIZE

        img = Image.open(os.path.join(folder, f))

        # Convert to RGBA if not already
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        images.append((x, y, img))
    except Exception as e:
        print(f"Skipping {f}: {e}")
        
# Determine size of stitched image
max_x = max(x + img.width for x, y, img in images)
max_y = max(y + img.height for x, y, img in images)

# Simple estimate: image size in bytes
memory_bytes_simple = max_x * max_y * 4  # 4 bytes per RGBA pixel

# Adjusted estimate (factor 2.5 for overhead)
memory_bytes_realistic = memory_bytes_simple * 2.2
memory_gb = memory_bytes_realistic / (1024**3)
print(f"Estimated RAM usage for stitched image: {memory_gb:.2f} GB")
# Create blank canvas
stitched = Image.new("RGBA", (max_x, max_y))

# Prompt user to continue or cancel based on config file
if prompt_continue:
    print("\nWARNING: The above RAM usage is only an estimate.")
    print("If this number is too high for your system, the script may fail or crash.")
    print("Press Enter to continue or Ctrl+C to cancel.")
    input()
    
# Paste all images onto canvas
for x, y, img in tqdm(images, desc="Stitching tiles", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}]"):
    stitched.paste(img, (x, y), img)
    
print("Saving the stitched tiles. This may take a moment.")

# Use safe filename generator (starts numbering at _0002)
output_path = get_safe_filename(output_folder, base_name="stitched", ext=".png", start_counter=2)

# Flag to tell the thread when saving is done
saving_done = False

def heartbeat():
    while not saving_done:
        print("Saving in progress... Please wait.")
        time.sleep(5)  # print every 5 seconds

# Start heartbeat in a separate thread
t = threading.Thread(target=heartbeat)
t.start()

# Save the large image (blocking)
stitched.save(output_path)

# Indicate saving is done
saving_done = True
t.join()

print(f"Saving complete! File saved to {output_path}")