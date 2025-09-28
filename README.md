# Wplace-Tile-Grabber-Combiner

This Python script will pull tiles from Wplace and save them for you.

## Features
- Change transparency of the saved tiles.
- Combine saved tiles into one large image.
- This script could use a lot of RAM. The script will attempt to estimate usage.

## Settings

| Setting                          | Type    | Options / Default           | Description                                                                                |
| -------------------------------- | ------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| `tiles_save_folder`              | string  | `"./images"`                | Your save location for the tiles.                                                          |
| `combined_save_folder`           | string  | `"./combined"`              | Your save location for the stitched tiles.                                                 |
| `prompt_continue_after_estimate` | boolean | `true` / `false`            | Whether you want to be prompted to continue after RAM estimate.                            |
| `start_tile_x`                   | integer | e.g., `550`                 | Starting tile X coordinate.                                                               |
| `start_tile_y`                   | integer | e.g., `750`                 | Starting tile y coordinate.                                                               |
| `end_tile_x`                     | integer | e.g., `600`                 | Ending tile x coordinate.                                                                 |
| `end_tile_y`                     | integer | e.g., `800`                 | Ending tile y coordinate.                                                                 |
| `placeholder.type`               | string  | `"transparent"` / `"solid"` | Whether you want missing tiles from Wplace to be filled with a transparent or solid color. |
| `placeholder.color`              | string  | e.g., `"#EC407A"`           | HEX value of the solid color (if type=`solid`).                                            |
| `replace_transparency.type`      | string  | `"transparent"` / `"solid"` | Whether you want to replace all transparent pixels of all saved tiles with a solid color.  |
| `replace_transparency.color`     | string  | e.g., `"#FF6F00"`           | HEX value of the solid color (if type=`solid`).                                            |
