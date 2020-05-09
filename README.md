# nbt-converter

A tool designed for Minecraft servers running [PGM](https://pgm.dev/) to convert levels created in Minecraft versions 1.9 to 1.12.2 down to 1.8 format. Uses [twoolie/NBT](https://github.com/twoolie/NBT) for inspecting and editing the Minecraft region files.

This does the absolute minimum to allow Minecraft maps created in newer versions (1.9 to 1.12.2) to be used in a 1.8 server environment by converting the NBT and ids (such as `minecraft:chest` to `Chest`) and so on. This tool is only intended to be used on levels used for PvP maps, not survival worlds. Make backups before using this script on your worlds. There is no guarantee that it will work flawlessly.

## What It Does

This script iterates over each of the world chunks looking for entities, tile entities, and blocks which are not compatible with Minecraft 1.8 and converts them by changing the ID names, NBT structure, or replacing it with something else that will work most appropriately in the context of Minecraft PvP. 

Certain objects have been provided with specific conversions, however, the script ties its best to convert incompatible objects that havn't been explicitly defined. You can see which [entities](https://github.com/mitchts/nbt-converter/blob/master/converter/entity.py), [tile entities](https://github.com/mitchts/nbt-converter/blob/master/converter/tileEntity.py), [blocks](https://github.com/mitchts/nbt-converter/blob/master/converter/block.py), and [items](https://github.com/mitchts/nbt-converter/blob/master/converter/item.py) are being converted in their respective files.

## Usage

Make sure you have Python installed. Recommended versions are 2.7, 3.4 to 3.7.

Open a terminal in the script location and run:

`python converter.py <dir> [options]`

Where `<dir>` is the Minecraft level file directory path, or a root directory for many Minecraft levels (if using the `-r` recursive option). Run `python converter.py --help` to see a full list of options.

```bash
$ python converter.py "C:\full\path\to\map\super_cool_map"
Version 1.2.10

Loading level at C:\full\path\to\map\super_cool_map
Level saved as Minecraft version 1.12
Made 2 modifications in Chunk 8,4 (in world at -24,4)
Made 2 modifications in Chunk 8,5 (in world at -24,5)
Made 2 modifications in Chunk 9,3 (in world at -23,3)
Made 1 modifications in Chunk 9,4 (in world at -23,4)
Made 2 modifications in Chunk 9,5 (in world at -23,5)
Made 2 modifications in Chunk 9,6 (in world at -23,6)
Made 2 modifications in Chunk 13,3 (in world at -19,3)
Made 1 modifications in Chunk 13,4 (in world at -19,4)
Made 1 modifications in Chunk 13,5 (in world at -19,5)
Made 2 modifications in Chunk 13,6 (in world at -19,6)
Made 2 modifications in Chunk 14,4 (in world at -18,4)
Made 2 modifications in Chunk 14,5 (in world at -18,5)
21 modifications made to the level nbt
0 modifications made to block section byte arrays
```

Warnings may be ignored, but should be investigated by the user to make sure the subject is working as intended. Please create an issue if something is not as it should be.

## Limitations

This tool will only support levels made for Minecraft 1.9 through to 1.12.2, nothing newer. Levels loaded in Minecraft 1.13 and above will need to use something like [Jupisoft111/Minecraft-Tools](https://github.com/Jupisoft111/Minecraft-Tools) to convert the level to 1.12.2 format. From there, you should be able to use this tool to convert the level to 1.8 format.

Any loss of levels falls on the user. There is no guarantee that this tool will convert everything perfectly, so it is up to you to create backups of the world before using this.
