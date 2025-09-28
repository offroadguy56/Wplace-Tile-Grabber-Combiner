# Wplace-Tile-Grabber-Combiner
This Python script will pull tiles from Wplace and save them for you.

The script offers the ability to change transparency of the saved tiles.
The script offers the ability to combine saved tiles into one large image.
Be warned this could use a lot of RAM. The script should warn you on the predicted RAM usage.  



The Settings:

"tiles_save_folder": "./images",           # Your save location for the tiles
  "combined_save_folder": "./combined",    # Your save location for the stitched tiles
  "prompt_continue_after_estimate": true   # Whether you want to be prompted to continue after RAM estimate
  "start_tile_x": 110,                     # Starting tile X coordinate
  "start_tile_y": 887,                     # Starting tile y coordinate
  "end_tile_x": 111,                       # Ending tile x coordinate
  "end_tile_y": 888,                       # Ending tile y coordinate
  "placeholder": {                   
    "type": "transparent",                 # Options are transparent or solid. Whether you want missing tiles from Wplace to be filled with a transparent or solid color
    "color": "#EC407A"                     # HEX value of the solid color
  },
  "replace_transparency": {
    "type": "transparent",                 # Options are transparent or solid. Whether you want to replace all transparent pixels of all saved tiles with a solid color
    "color": "#FF6F00"                     # HEX value of the solid color
