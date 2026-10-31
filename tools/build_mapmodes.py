"""Builds conqueror-map-mode/gui/00_tmm_mapmodes.gui from vanilla gui/shared/mapmodes.gui.

Copies the type flowcontainer_additional_mapmodes verbatim (CRLF kept) and inserts the
TMM button after the legends map mode button. Re-run after each CK3 patch.
"""
import re
import sys

VANILLA = r"G:/SteamLibrary/steamapps/common/Crusader Kings III/game/gui/shared/mapmodes.gui"
OUT = r"C:/Users/Akiway/Documents/Paradox Interactive/Crusader Kings III/mod/conqueror-map-mode/gui/00_tmm_mapmodes.gui"

raw = open(VANILLA, "rb").read().decode("utf-8-sig")
lines = raw.split("\r\n")

start = next(i for i, l in enumerate(lines) if l.startswith("\ttype flowcontainer_additional_mapmodes = "))
end = next(i for i in range(start + 1, len(lines)) if lines[i] == "\t}")
block = lines[start:end + 1]

# Insert after the closing brace of the legends button
leg = next(i for i, l in enumerate(block) if 'name = "map_mode_legends_button"' in l)
close = next(i for i in range(leg, len(block)) if block[i] == "\t\t\t\t}")

T = "\t\t\t\t"
button = f"""{T}# TMM start - Trait map: opens the tmm_trait_map situation view
{T}widget = {{
{T}	name = "tmm_map_mode_button"
{T}	parentanchor = vcenter
{T}	size = {{ 32 32 }}
{T}	datacontext = "[GetSituation( 'tmm_trait_map' )]"
{T}	visible = "[CanChangeMapMode]"

{T}	icon = {{
{T}		size = {{ 100% 100% }}
{T}		texture = "gfx/interface/component_masks/mask_circle.dds"
{T}		visible = "[And( Situation.IsValid, IsMapMode( 'situation' ) )]"

{T}		glow = {{
{T}			color = {{ 0.93 0.65 0.45 1.0 }}
{T}			glow_radius = 6

{T}			glow_generation_rules = {{
{T}				glow_alpha_mask = 0
{T}				glow_blur_passes = 15
{T}				glow_texture_downscale = 5.5f
{T}				glow_ignore_inside_pixels = yes
{T}			}}
{T}		}}

{T}		using = Animation_Glow_Pulse
{T}	}}

{T}	button_round = {{
{T}		visible = "[Situation.IsValid]"
{T}		size = {{ 100% 100% }}
{T}		using = tooltip_nw
{T}		onclick = "[ToggleGameViewData( Situation.GetWindowName, Situation.GetID )]"
{T}		tooltip = "TMM_MAP_MODE_BUTTON_TT"

{T}		icon = {{
{T}			parentanchor = center
{T}			size = {{ 24 24 }}
{T}			alwaystransparent = yes
{T}			texture = "gfx/interface/icons/message_feed/trait.dds"
{T}		}}
{T}	}}

{T}	button_round = {{
{T}		visible = "[Not( Situation.IsValid )]"
{T}		size = {{ 100% 100% }}
{T}		using = tooltip_nw
{T}		onclick = "[GetScriptedGui( 'tmm_start_situation' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
{T}		enabled = "[GetScriptedGui( 'tmm_start_situation' ).IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
{T}		tooltip = "TMM_MAP_MODE_BUTTON_START_TT"

{T}		icon = {{
{T}			parentanchor = center
{T}			size = {{ 24 24 }}
{T}			alwaystransparent = yes
{T}			alpha = 0.5
{T}			texture = "gfx/interface/icons/message_feed/trait.dds"
{T}		}}
{T}	}}
{T}}}
{T}# TMM end""".split("\n")

block = block[:close + 1] + button + block[close + 1:]

header = [
    "# Trait Map Mode - override of the type flowcontainer_additional_mapmodes",
    "# from gui/shared/mapmodes.gui (vanilla 1.20.0.4). GUI types are registered by the",
    "# first file that declares them and gui/00_* loads before gui/shared/*.",
    "# Only the lines between 'TMM start' and 'TMM end' differ from vanilla.",
    "types TmmMapModes",
    "{",
]
out = "\r\n".join(header + block + ["}"])
open(OUT, "wb").write(("\ufeff" + out).encode("utf-8"))
print("type lines", start + 1, end + 1, "inserted after block line", close + 1, "total", len(header + block) + 1)
