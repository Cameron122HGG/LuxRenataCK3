"""Lux Renata bookmark helper: filler art and a CK2-style character row.

Every bookmark needs gfx/interface/bookmarks/<bookmark>.dds (the background) and
<bookmark>_<character name>.dds (the image shown when that character is hovered or selected).
For each bookmark in common/bookmarks/bookmarks/*.txt this copies LR_bookmark_filler.dds into
any of those files that are missing, so a new bookmark only needs its script.

With --layout, the characters of bookmarks that use the filler art (or the bookmarks named on
the command line) are laid out in a row along the filler's bottom band, like CK2's recommended
characters: one centred row, spaced to fit. Only their `position = { x y }` lines are rewritten.

Usage, from the mod folder:
    python tools/LR_bookmark_art.py                     # fill in missing art for every bookmark
    python tools/LR_bookmark_art.py --layout            # ...and lay out the filler bookmarks
    python tools/LR_bookmark_art.py --layout bm_x bm_y  # lay out just these bookmarks
    python tools/LR_bookmark_art.py --dry-run           # report only
"""
import os, re, sys, glob, shutil

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(MOD, "gfx", "interface", "bookmarks")
FILLER = os.path.join(ART, "LR_bookmark_filler.dds")

# The row sits in the filler's bottom band (1920x1080 canvas; a position is the portrait's top-left corner)
ROW_Y = 852
ROW_LEFT, ROW_RIGHT = 160, 1760
SLOT_MAX = 210          # widest spacing between portraits
PORTRAIT_HALF = 70      # half a portrait's width, to centre it on its slot


def blocks(text):
    """Top-level `key = { ... }` blocks: (key, start, end)."""
    out = []
    for m in re.finditer(r"^(\w+)\s*=\s*\{", text, re.M):
        if out and m.start() < out[-1][2]:
            continue
        i, d = m.end(), 1
        while d and i < len(text):
            c = text[i]
            if c == "#":
                j = text.find("\n", i); i = len(text) if j < 0 else j; continue
            d += (c == "{") - (c == "}"); i += 1
        out.append((m.group(1), m.start(), i))
    return out


def row_positions(n):
    span = ROW_RIGHT - ROW_LEFT
    step = min(SLOT_MAX, span // max(n, 1))
    first = (ROW_LEFT + ROW_RIGHT) // 2 - step * (n - 1) // 2
    return [(first + i * step - PORTRAIT_HALF, ROW_Y) for i in range(n)]


def main(argv):
    dry = "--dry-run" in argv
    layout = "--layout" in argv
    only = [a for a in argv if not a.startswith("--")]
    if not os.path.exists(FILLER):
        sys.exit("missing " + FILLER)
    for path in sorted(glob.glob(os.path.join(MOD, "common", "bookmarks", "bookmarks", "*.txt"))):
        raw = open(path, "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf"); crlf = b"\r\n" in raw
        text = raw[3 if bom else 0:].decode("utf-8").replace("\r\n", "\n")
        changed = False
        for key, s, e in reversed(blocks(text)):
            body = text[s:e]
            if "start_date" not in body:
                continue
            names = re.findall(r'^\s*name\s*=\s*"?(\w+)"?', body, re.M)
            bg = os.path.join(ART, key + ".dds")
            uses_filler = not os.path.exists(bg)
            todo = [bg] if uses_filler else []
            todo += [p for p in (os.path.join(ART, "%s_%s.dds" % (key, n)) for n in names) if not os.path.exists(p)]
            for p in todo:
                print(("would copy" if dry else "copy"), "filler ->", os.path.relpath(p, MOD))
                if not dry:
                    shutil.copyfile(FILLER, p)
            if layout and names and ((only and key in only) or (not only and uses_filler)):
                pos = iter(row_positions(len(re.findall(r"^\s*position\s*=\s*\{", body, re.M))))
                new_body = re.sub(r"^(\s*position\s*=\s*)\{[^}]*\}", lambda m: "%s{ %d %d }" % ((m.group(1),) + next(pos)), body, flags=re.M)
                if new_body != body:
                    print(("would lay out" if dry else "laid out"), key, "(%d characters)" % len(names))
                    text = text[:s] + new_body + text[e:]; changed = True
        if changed and not dry:
            out = text.replace("\n", "\r\n") if crlf else text
            open(path, "wb").write((b"\xef\xbb\xbf" if bom else b"") + out.encode("utf-8"))


if __name__ == "__main__":
    main(sys.argv[1:])
