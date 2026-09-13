"""Rebuilds thumbnail.png (Workshop preview) and thumbnail-200px.png (a legibility check
at Steam's listing size, not uploaded). Layout lives in thumbnail_layout.py.

Placeholder version, no screenshots needed: the title band over a crop of AGOT's own
paper map (flatmap.dds, read from the Workshop copy of AGOT) with two labels.

For a real before/after take two F12 screenshots of the same AGOT camera position on
zoom step 9 or 10 (holdings gone with the base mod alone, holdings still there with
this patch), then:
    from thumbnail_layout import make
    make(OUT, "AGOT PATCH", OLD, NEW, CROP, CROP, sub="SMOOTH ZOOM TRANSITIONS")
with CROP in 5120x1440 screenshot coordinates, clear of the HUD."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from thumbnail_layout import S, BAND, GOLD, CREAM, DARK, fit, label, finish

AGOT = os.path.expanduser("~/.local/share/Steam/steamapps/workshop/content/1158310/2962333032")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "thumbnail.png")
MAP_CROP = (3400, 2900, 6100, 5112)     # Blackwater Bay and the Crownlands, 1.22:1 like the body area

def main():
    body_h = S - BAND
    flat = Image.open(AGOT + "/gfx/map/terrain/flat_maps/flatmap.dds").convert("RGB").crop(MAP_CROP).resize((S, body_h), Image.LANCZOS)
    canvas = Image.new("RGB", (S, S), DARK[:3])
    canvas.paste(flat, (0, BAND))
    d = ImageDraw.Draw(canvas, "RGBA")
    title, sub = "AGOT PATCH", "SMOOTH ZOOM TRANSITIONS"
    f_title = fit(d, title, 92, S - 60); f_sub = fit(d, sub, 58, S - 60)
    tw = d.textlength(title, font=f_title); d.text(((S - tw) / 2, 18), title, font=f_title, fill=CREAM)
    sw = d.textlength(sub, font=f_sub); d.text(((S - sw) / 2, 118), sub, font=f_sub, fill=GOLD)
    d.rectangle([0, BAND - 4, S, BAND], fill=GOLD)
    f_tag = fit(d, "FOR A GAME OF THRONES", 84, S - 52 - 44)
    tag_h = f_tag.size + 22 * 2 - 10
    label(d, S - 2 * tag_h - 44, "FOR A GAME OF THRONES", f_tag)
    label(d, S - tag_h - 22, "TOWNS STAY ON THE MAP", f_tag)
    finish(canvas, OUT)

if __name__ == "__main__":
    main()
