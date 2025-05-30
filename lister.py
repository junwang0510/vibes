import os
import json
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

input_dir = "images"

# 1) Convert all HEIC → JPG & delete originals
for fname in os.listdir(input_dir):
    if fname.lower().endswith(".heic"):
        src = os.path.join(input_dir, fname)
        im = Image.open(src)
        new_name = os.path.splitext(fname)[0] + ".jpg"
        dst = os.path.join(input_dir, new_name)
        im.convert("RGB").save(dst, "JPEG")
        os.remove(src)

# 2) Scan folder once for final widths/heights, deduplicated
output = {}
for fname in os.listdir(input_dir):
    fp = os.path.join(input_dir, fname)
    try:
        im = Image.open(fp)
        output[fname] = [im.width, im.height]
    except:
        continue

with open("image_widths_heights.json", "w") as f:
    # list-of-[name,[w,h]]
    json.dump([[n, dims] for n, dims in output.items()], f, indent=2)

print(f"Wrote {len(output)} entries to image_widths_heights.json")