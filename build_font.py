"""Rebuild the NOVEMBER_BORDER bitmap font (used by every TextMesh) with CJK glyphs.

Usage: python build_font.py <charset.txt> <out_sharedassets0.assets> [preview.png]
Original glyphs are copied over untouched; every other character is rendered with
Source Han Sans, binarized and given the same 2px black outline as the pixel font.
"""
import sys

import UnityPy
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from UnityPy.enums import TextureFormat

SRC = r"e:\T File\SNE_WORK\backup\sharedassets0.assets"
CJK_FONT = r"e:\T File\SNE_WORK\fonts\SourceHanSansCN-Bold.otf"
FONT_ID = 97
TEX_ID = 19

CELL_H = 32
CJK_PX = 28
OUTLINE = 2
CJK_ADVANCE = CJK_PX + OUTLINE * 2
PAD = 1


def render_cjk(ch, font):
    """Return a CJK_ADVANCE x CELL_H RGBA glyph with white fill and black outline."""
    canvas = Image.new("L", (CJK_ADVANCE, CELL_H), 0)
    left, top, right, bottom = font.getbbox(ch)
    if right <= left or bottom <= top:
        return None
    ascent, descent = font.getmetrics()
    em_top = (CELL_H - (ascent + descent)) // 2 + 1
    x = OUTLINE + (CJK_PX - font.getlength(ch)) / 2
    ImageDraw.Draw(canvas).text((x, em_top), ch, font=font, fill=255)
    fill = canvas.point(lambda v: 255 if v >= 110 else 0)
    outline = fill.filter(ImageFilter.MaxFilter(OUTLINE * 2 + 1))
    glyph = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glyph.paste((0, 0, 0, 255), mask=outline)
    glyph.paste((255, 255, 255, 255), mask=fill)
    return glyph


def main(charset_path, out_path, preview_path=None):
    with open(charset_path, encoding="utf-8") as f:
        wanted = sorted({c for c in f.read() if ord(c) > 126 and not c.isspace()})

    env = UnityPy.load(SRC)
    objs = {o.path_id: o for o in env.objects}
    font_obj = objs[FONT_ID]
    tree = font_obj.read_typetree()
    tex = objs[TEX_ID].read()
    old_img = tex.image.convert("RGBA")
    ow, oh = old_img.size

    existing = {r["index"] for r in tree["m_CharacterRects"]}
    wanted = [c for c in wanted if ord(c) not in existing]

    glyphs = []
    for r in tree["m_CharacterRects"]:
        uv = r["uv"]
        gw, gh = round(uv["width"] * ow), round(uv["height"] * oh)
        left = round(uv["x"] * ow)
        top = oh - round(uv["y"] * oh) - gh
        glyphs.append((r, old_img.crop((left, top, left + gw, top + gh))))

    font = ImageFont.truetype(CJK_FONT, CJK_PX)
    missing = []
    for ch in wanted:
        g = render_cjk(ch, font)
        if g is None:
            missing.append(ch)
            continue
        rect = {
            "index": ord(ch),
            "uv": None,
            "vert": {"x": 0.0, "y": 0.0, "width": float(CJK_ADVANCE), "height": -float(CELL_H)},
            "width": float(CJK_ADVANCE),
            "flipped": False,
        }
        glyphs.append((rect, g))

    width, height = next(s for s in ATLAS_SIZES if fits(glyphs, *s))
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = y = 0
    rects = []
    for rect, img in glyphs:
        w, h = img.size
        if x + w > width:
            x, y = 0, y + CELL_H + PAD
        atlas.paste(img, (x, y))
        rect = dict(rect)
        rect["uv"] = {"x": x / width, "y": 1 - (y + h) / height, "width": w / width, "height": h / height}
        rects.append(rect)
        x += w + PAD

    tex.set_image(atlas, target_format=TextureFormat.ARGB32)
    tex.save()
    tree["m_CharacterRects"] = rects
    font_obj.save_typetree(tree)

    with open(out_path, "wb") as f:
        f.write(env.file.save())
    if preview_path:
        atlas.crop((0, 0, min(width, 1024), min(height, 512))).save(preview_path)
    print(f"atlas {width}x{height}, glyphs {len(rects)}, new cjk {len(wanted) - len(missing)}, missing {''.join(missing)!r}")


ATLAS_SIZES = [(256, 256), (512, 512), (1024, 1024), (2048, 2048), (4096, 2048), (4096, 4096)]


def fits(glyphs, width, height):
    x = y = 0
    for _, img in glyphs:
        w, _ = img.size
        if x + w > width:
            x, y = 0, y + CELL_H + PAD
        x += w + PAD
    return y + CELL_H <= height


if __name__ == "__main__":
    main(*sys.argv[1:])
