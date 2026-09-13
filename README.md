# AGOT Patch for Smooth Zoom Transitions (CK3)

A compatibility patch that makes
[Smooth Zoom Transitions](https://github.com/mekedron/ck3-zoom-transition-fix)
work on the map of the
[A Game of Thrones](https://steamcommunity.com/sharedfiles/filedetails/?id=2962333032)
total conversion. Without it the base mod, loaded below AGOT, makes every holding
model on the AGOT map vanish on zoom step 8 - long before the realm colours start
filling the map - and leaves AGOT's roads, special buildings and animals on layers
that its table does not declare. The patch also stops AGOT drawing every holding
model until step 16, far into the painted political map.

<img src="thumbnail.png" alt="AGOT Patch for Smooth Zoom Transitions" width="360">

## Why AGOT needs a patch

Smooth Zoom Transitions is tuned for vanilla's zoom and ships a full copy of the vanilla
`gfx/map/map_object_data/game_object_layers.txt` with its three layers moved off zoom
step 9. AGOT replaces the same file and the camera behind it, and the two do not agree:

| | vanilla | Smooth Zoom | AGOT |
| --- | --- | --- | --- |
| `building_layer` unloads on step | 9 | 8 | **16** |
| layers in the file | 3 | 3 | **7** (adds `AGOT_building_layer`, `AGOT_roads`, `AGOT_low_roads`, `AGOT_animal_layer`) |
| camera height on step 8 / 9 / 16 | 344 / 396 / 865 | same | **250 / 300 / 793** (`ZOOM_STEPS` in `common/defines/graphic/00_graphics.txt`) |
| large map names from step | 9 | 11 | **12** |

So with AGOT above Smooth Zoom, Smooth Zoom's table wins and:

* holdings unload on step 8, 250 units up on AGOT's camera, where AGOT keeps them until
  step 16. AGOT's realm colour overlay only starts on step 9 (10 with the base mod), so
  the towns and villages disappear from a map that is still plain terrain;
* the 64 special buildings (Pyke's bridge, the Wall's castles, the Bridge of Skulls...),
  the 74 road objects and the 21 animal objects sit on layers the table does not declare.
  What the engine does with objects on an undeclared layer is not verified here; at
  best they lose their fade step.

With AGOT *below* Smooth Zoom, AGOT's table wins and the buildings are fine, but the base
mod's step 9 clean-up does not happen for AGOT's layers, and its map name step (11)
overrides AGOT's (12) regardless of mod order, because defines files are read in file
name order.

## What the patch is

Two layer tables and one defines file, AGOT's numbers with the base mod's idea applied to
them: nothing that AGOT unloads together with the two low tree layers on step 9 stays
there, and the holding models leave when the realm colours arrive instead of six steps
later.

| file | what |
| --- | --- |
| `gfx/map/map_object_data/game_object_layers.txt` | AGOT's seven layers; `activities_layer` 9 → 7, `AGOT_animal_layer` 9 → 8, `unit_layer` 9 → 10, `building_layer`, `AGOT_building_layer`, `AGOT_roads`, `AGOT_low_roads` 16 → 10; plus a new `AGOT_skybox_layer` on 16 |
| `gfx/map/map_object_data/skyx_skybox.txt` | AGOT's file with the skybox moved to `AGOT_skybox_layer`, so it keeps AGOT's step 16 while the building layer it used to share goes on 10 |
| `gfx/map/map_object_data/effect_layers.txt` | coast foam 9 → 7, mountain env effects 9 → 8 (the base mod uses 6 and 7; AGOT's camera is lower at the same step, so the same heights are one step later) |
| `common/defines/graphic/zz_smooth_zoom_agot.txt` | `LARGE_NAMES_ZOOM_STEP` back to AGOT's 12 |
| `common/defines/graphic/zz_smooth_zoom_agot_ultrawide.txt.off` | opt-in, see below |

The rest of the base mod applies to AGOT unchanged and is not duplicated here: the
streaming budget (`MAX_MESHES_LOADED_PER_FRAME` 100 → 50), the colour overlay start
(9 → 10), the fort and raid icons (9 → 10), the flat map icon work, the border update
interval and the name placement search all override keys that AGOT sets to the vanilla
values. That is why the base mod must stay enabled.

Both layer files start with a `#` comment listing every value against AGOT's;
`tools/diff_agot.sh` prints the differences against the Workshop copy of AGOT, for
carrying the change over after an AGOT update.

On AGOT's camera, the zoom steps the patch uses:

| step | 6 | 7 | 8 | 9 | 10 | 12 | 16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| camera height | 179 | 210 | 250 | 300 | 355 | 468 | 793 |
| unloads / switches | grass | activities, coast foam | animals, mountain and other env effects | `tree_low`, `tree_medium` | holdings, AGOT's cities, roads and bridges, armies, colour overlay starts, fort and raid icons, AGOT's fog of war fade | large map names | skybox, `tree_high` |

### Why the holdings leave on step 10

AGOT keeps `building_layer` until step 16, 793 units up, when the realm colour overlay has
been fully opaque since step 15 and the map reads as a painted political map. Every castle,
city and temple on the screen is still a mesh instance at that height, over an area many
times what vanilla ever draws holdings on, and that is where a 4 GB laptop GPU dropped from
60 to 17 FPS on the AGOT map. Step 10 is where the overlay starts filling (the base mod
moves it there from 9), so the models go as the colours come.

AGOT's hand placed cities are not holdings: Braavos, Gulltown, Lannisport, Tyrosh,
Oldtown, White Harbor, Pentos, Pyke and the Wall's castles are map objects on AGOT's own
`AGOT_building_layer`, and the bridges and Valyrian roads on `AGOT_roads` /
`AGOT_low_roads`. Those go on step 10 as well, so no town outlives the colour fill while
King's Landing and every barony have already gone. AGOT's skybox mesh shares
`AGOT_building_layer`; it is moved to a layer of its own with AGOT's step 16, or the sea
beyond the map edge would lose its sky on step 10. `fade_out` is one number per layer in
`game_object_layers.txt` if you want any of them back longer.

Not covered: 3D landmarks that other mods add as *building assets* (COW-AGOT's Maidenpool,
for one) are drawn by the holding system, not by a map object layer, and this patch has no
say over when they unload.

### Ultrawide extra (opt-in)

The base mod's opt-in file cuts `NAME_DRAW_DISTANCE` from vanilla's 12000 to 9000. AGOT
sets 20000 for its larger map, so that file would cut the radius by more than half on
AGOT. Rename `zz_smooth_zoom_agot_ultrawide.txt.off` to `.txt` instead: it applies the
same three quarters to AGOT's value (15000) and sorts after the base mod's file, so it
wins if both are enabled.

## Load order

    A Game of Thrones
    Smooth Zoom Transitions          (anywhere; above or below AGOT both work)
    AGOT Patch for Smooth Zoom Transitions   (below AGOT)

Only the last line matters: the patch replaces AGOT's layer file, so it has to be below
AGOT. The defines files of both mods are picked up wherever the mods sit.

## Layout

    descriptor.mod                              mod metadata
    thumbnail.png                               Workshop preview, must sit in the mod root
    common/defines/graphic/zz_smooth_zoom_agot.txt   map name step
    common/defines/graphic/zz_*_ultrawide.txt.off    opt-in name radius
    gfx/map/map_object_data/game_object_layers.txt   AGOT's game object layers, retuned
    gfx/map/map_object_data/effect_layers.txt        effect layers, retuned
    install.sh                                  copies the mod into the Proton prefix
    tools/check_log.sh                          mount check and error.log grep after a game start
    tools/diff_agot.sh                          diff against the Workshop copy of AGOT
    tools/bbcode_to_plain.py                    regenerates the Paradox Mods texts
    steam-workshop/                             listing texts and the thumbnail generator

## Installing

Run `./install.sh`. It copies the mod into the CK3 mod directory inside the Proton
prefix. Then, in the launcher playset, enable it below A Game of Thrones, with Smooth
Zoom Transitions enabled too. No shader is touched, so there is no recompile; the change
is visible on the first zoom.

## File encoding

Every `.txt` here starts with a UTF-8 BOM, like the vanilla and AGOT files. Without it
the game still reads them, but logs one `should be in utf8-bom encoding` line per file.

## Game version

Built against CK3 1.19.0.6 (Scribe), AGOT 0.5.2.1 and Smooth Zoom Transitions 1.0.0.
After an AGOT release run `tools/diff_agot.sh`: if AGOT changed its layer list or its
`ZOOM_STEPS`, the two tables here need the same change.

## Multiplayer / achievements

Map object layers and graphics defines are not checksummed content, but the launcher still
marks any mod as a mod. Treat it like any other graphics mod.
