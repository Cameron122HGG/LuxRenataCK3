# Lux Renata — playing with a controller (Steam Input)

CK3 on PC can't bind gamepad buttons in its own files (tested 2026-11-06: `GAMEPAD_*` names in
`shortcuts.shortcuts` are silently ignored). So:

- **Steam Input** turns the controller into keyboard and mouse.
- **Lux Renata's Command Menu** (press **Insert**) puts the main windows, map modes and time controls
  on big buttons, so one controller button reaches all of them.

## Setup

1. Steam → Library → Crusader Kings III → ⚙ → Properties → Controller → **Enable Steam Input**.
2. ⚙ → Controller Layout → Edit Layout, then set the buttons as below (Xbox names; PlayStation in brackets).
3. Save it as a personal layout called "Lux Renata" (or export/share it from the same screen).

## Layout

| Control | Steam Input setting | In game |
|---|---|---|
| Left stick | **Joystick Mouse** | Move the cursor |
| Right stick | **Directional Pad** → Up/Down/Left/Right arrow keys | Pan the map |
| A (✕) | Left mouse click | Select / press |
| X (□) | Right mouse click | Right-click actions (e.g. interaction menu) |
| B (○) | Escape | Close the window |
| Y (△) | **Insert** | **Open / close the Command Menu** |
| LB (L1) | Z | Slower |
| RB (R1) | X | Faster |
| LT (L2) | Page Up | Zoom out |
| RT (R2) | Page Down | Zoom in |
| D-pad Up / Down | Mouse wheel up / down | Scroll lists and windows |
| D-pad Left | B | Back (previous character or title) |
| D-pad Right | F1 | My character |
| Start (Options) | Space | Pause / resume |
| View / Back (Touchpad) | Home | Go to capital |
| Left stick click (L3) | Return | Confirm |
| Right stick click (R3) | C | Find a character |

Optional extras for the Steam layout editor:
- On LB and RB, leave "Turbo" and "Repeat" off so each press changes speed by one step.
- Use a Mode Shift (for example, hold LT) to put the de jure map modes (shift+Q/W/E) on the face buttons.
- For a cursor that is precise on the map, set the left stick's Joystick Mouse sensitivity to ~120% and
  set the output curve to "Aggressive".

## The Command Menu

Press **Y** (Insert). It shows three columns:

- **Windows:** Character, Realm, Military, Council, Court, Intrigue, Factions, Decisions, Activities,
  Situations. Picking one opens it and closes the menu.
- **Map Modes:** Realms, de jure Duchies/Kingdoms/Empires/Hegemonies, Cultures, Faiths, Houses, Terrain,
  Development. The menu stays open so you can flip through them.
- **Time:** Pause, Faster, Slower (the menu stays open) and Go to Capital (the menu closes).

Close it with **Y** again, **B** (Escape), or the ✕ in its header.

## Troubleshooting

- **The cursor moves twice as fast, or the camera moves along with the cursor:** CK3's own gamepad
  cursor may also be reading the pad through Steam's virtual controller. Lower the stick's Joystick Mouse
  sensitivity, or in `Documents/Paradox Interactive/Crusader Kings III/pdx_settings.txt` set
  `"ingame_gamepad_navigation_support"` to `enabled=no` (untested).
- **Arrow keys don't pan the map:** bind the right stick to W/A/S/D instead.
- **Insert does nothing:** check that the pause menu is closed. The menu doesn't open over the pause menu.
- **A key in the table does something else:** keys can be rebound in CK3's `shortcuts.shortcuts`;
  change the Steam binding to match.
