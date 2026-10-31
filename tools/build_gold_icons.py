"""Bakes gold versions of vanilla flat icons for the participant groups.

Same result as the vanilla GUI type icon_flat_standard_gold (gui/shared/icons.gui):
frame 1 of gfx/interface/colors/colors_textured.dds added (blend_mode = add) onto
the black flat icon. Baked into files because the participant list is the vanilla
window_situation_participant_groups, which draws the group icon as is.
Output: uncompressed BGRA32 DDS, like most vanilla gfx/interface files.
"""
import os
import struct

from PIL import Image, ImageChops

GAME = r"G:/SteamLibrary/steamapps/common/Crusader Kings III/game"
MOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ICONS = {
    "gfx/interface/icons/flat_icons/star.dds": "gfx/interface/icons/situations/tmm/tmm_group_holders.dds",
    "gfx/interface/icons/flat_icons/vassal.dds": "gfx/interface/icons/situations/tmm/tmm_group_subjects.dds",
}


def write_dds(path, im):
    w, h = im.size
    hdr = struct.pack(
        "<4sIIIIIII44sIIIIIIIIIIIII", b"DDS ", 124, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8, h, w, w * 4, 0, 0, b"\0" * 44,
        32, 0x1 | 0x40, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000, 0x1000, 0, 0, 0, 0)
    r, g, b, a = im.split()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(hdr + Image.merge("RGBA", (b, g, r, a)).tobytes())


atlas = Image.open(os.path.join(GAME, "gfx/interface/colors/colors_textured.dds")).convert("RGBA")
gold = atlas.crop((0, 0, 96, 96))  # frame 1 (framesize 96x96)

for src, dst in ICONS.items():
    icon = Image.open(os.path.join(GAME, src)).convert("RGBA")
    tint = gold.resize(icon.size, Image.LANCZOS).convert("RGB")
    rgb = ImageChops.add(icon.convert("RGB"), tint)
    out = Image.merge("RGBA", (*rgb.split(), icon.getchannel("A")))
    write_dds(os.path.join(MOD, dst), out)
    print(dst, out.size)
