import os
import json
try:
    from PIL import Image
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError as e:
    print("Got import error", e)
    print("You need to install pillow and pillow-heif: `pip3 install pillow pillow-heif`")
    import sys; sys.exit(1)

input_dir = "images"
output_files = []

for file in os.listdir(input_dir):
    filepath = os.path.join(input_dir, file)
    try:
        im = Image.open(filepath)
        width, height = im.width, im.height

        # Convert HEIC to JPG and delete original
        if file.lower().endswith(".heic"):
            new_file = os.path.splitext(file)[0] + ".jpg"
            new_path = os.path.join(input_dir, new_file)
            im.convert("RGB").save(new_path, "JPEG")
            os.remove(filepath)  # Delete original HEIC file
            output_files.append([new_file, [width, height]])
        else:
            output_files.append([file, [width, height]])
    except:
        continue

json.dump(output_files, open("image_widths_heights.json", 'w'))
print(f"Successfully created image_widths_heights.json with {len(output_files)} files.")
