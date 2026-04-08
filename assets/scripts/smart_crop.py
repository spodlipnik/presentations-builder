"""smart_crop.py — Center-crop an image to an exact box aspect ratio.

Usage:
    python3 smart_crop.py <image_path> <box_width> <box_height> <output_path>

The box dimensions are in inches (matching PptxGenJS coordinates).
The script crops the image to match the box's aspect ratio using a center crop,
then saves as JPEG at 95% quality.

Used by talk-slides to implement `fit: cover` without relying on pptxgenjs's
broken `sizing` property.
"""

import sys
from PIL import Image


def smart_crop(img_path: str, box_w: float, box_h: float, out_path: str) -> None:
    im = Image.open(img_path)
    iw, ih = im.size
    box_ratio = box_h / box_w
    img_ratio = ih / iw

    if box_ratio > img_ratio:
        # Box is taller than image — crop width
        new_w = int(ih / box_ratio)
        left = (iw - new_w) // 2
        crop = im.crop((left, 0, left + new_w, ih))
    else:
        # Box is wider than image — crop height
        new_h = int(iw * box_ratio)
        top = (ih - new_h) // 2
        crop = im.crop((0, top, iw, top + new_h))

    # Convert RGBA to RGB (JPEG doesn't support alpha)
    if crop.mode == "RGBA":
        bg = Image.new("RGB", crop.size, (255, 255, 255))
        bg.paste(crop, mask=crop.split()[3])
        crop = bg

    crop.save(out_path, quality=95)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <image_path> <box_width> <box_height> <output_path>")
        sys.exit(1)

    smart_crop(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
