"""
Downscale + recompress the Wage Boost (sample_project) slide PNGs.

These were rendered at 2880x1620 and barely compressed (avg ~2.2 MB each,
~44 MB for the deck). Every other deck is 1920x1080 at ~200-400 KB. The
oversized deck overwhelmed the browser's per-host connection limit on scroll,
so some images stalled and rendered as broken-image icons.

This resizes them to 1920x1080 (same 16:9, plenty sharp for slide viewing)
and saves optimized PNGs, bringing the deck in line with the others.
"""
import glob
import os

from PIL import Image

SRC = "C:/Users/raeda/Downloads/PM_Final_StudyBook/slides/sample_project"
TARGET_W = 1920

before_total = 0
after_total = 0
files = sorted(glob.glob(SRC + "/*.png"))
for f in files:
    before = os.path.getsize(f)
    before_total += before
    im = Image.open(f).convert("RGB")
    w, h = im.size
    if w > TARGET_W:
        new_h = round(h * TARGET_W / w)
        im = im.resize((TARGET_W, new_h), Image.LANCZOS)
    im.save(f, "PNG", optimize=True, compress_level=9)
    after = os.path.getsize(f)
    after_total += after
    print(f"{os.path.basename(f):16} {w}x{h} -> {im.size[0]}x{im.size[1]}  "
          f"{before//1024:5} KB -> {after//1024:4} KB")

print(f"\nDeck total: {before_total//1024//1024} MB -> {after_total//1024} KB "
      f"({after_total//1024//1024} MB)  saved {(before_total-after_total)//1024//1024} MB")
