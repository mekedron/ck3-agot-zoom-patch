# Steam Workshop publishing kit

Everything needed for the Steam Workshop and Paradox Mods listings. Nothing here ships with the mod
itself — the mod is `descriptor.mod`, `thumbnail.png`, `common/` and `gfx/` in the repository root.

| File | Where it goes |
| --- | --- |
| `description-en.txt` | Workshop item description (BBCode) |
| `description-ru.txt` | Russian version of the same description |
| `description-paradoxmods-en.txt` | same text without BBCode, for the Paradox Mods site |
| `description-paradoxmods-ru.txt` | Russian version without BBCode |
| `short-description-en.txt` | Launcher / Paradox Mods short description, under 200 chars |
| `short-description-ru.txt` | Russian short description, under 200 chars |
| `make_thumbnail.py` | rebuilds `thumbnail.png` (placeholder from AGOT's paper map, or before/after from two screenshots) |
| `thumbnail_layout.py` | the shared layout module |

The `description-paradoxmods-*.txt` files are generated from the BBCode ones by
`tools/bbcode_to_plain.py`; edit the BBCode version first, then regenerate.

## Listing metadata

* **Title:** AGOT Patch for Smooth Zoom Transitions
* **Tags:** Fixes, Graphics, Utilities — same as `descriptor.mod`
* **Version:** 1.0.0, `supported_version="1.19.*"`
* **Visibility:** public
* **Required items:** A Game of Thrones (2962333032), Smooth Zoom Transitions (3800395737)

Short descriptions are kept under the launcher's 200 character limit; the Russian
description is well under Steam's 8000 byte limit.

## Preview image on Steam

The launcher picks up `thumbnail.png` from the mod root (next to `descriptor.mod`), which is
what `picture="thumbnail.png"` in the descriptor points at. The uploader form's own image
field applies to Paradox Mods, not to Steam. After changing it, re-run `install.sh` and
upload the mod again from the launcher.

The current image is a placeholder: the title band over a crop of AGOT's paper map with
two labels. `make_thumbnail.py` says how to build a real before/after from two screenshots
on zoom step 9 or 10 (holdings gone with the base mod alone, still there with the patch).

`thumbnail.png` is 1024x1024, quantised to 256 colours to stay under Steam's 1 MB limit,
and rebuilt from raw pixels so it carries no metadata. `thumbnail-200px.png` is a legibility
check at listing size and is not uploaded.

**Do not use `[code]` in the Steam files.** Steam renders it as a full-width block.
