# nbt-converter

A tool to convert maps created in newer Minecraft versions (1.9 to 1.12.2) to be usable in 1.8 for [Walrus Network](https://github.com/walrus-network). Uses [twoolie/NBT](https://github.com/twoolie/NBT) for inspecting and editing the Minecraft region files.

This does the absolute minimum to allow Minecraft maps created in newer versions (1.9 to 1.12.2) to be used in a 1.8 server environment by converting the NBT and ids (such as `minecraft:chest` to `Chest`) and so on. This tool is only intended to be used on levels used for PvP maps, not survival worlds. Make backups before using this script on your worlds. There is no guarantee that it will work flawlessly.

## What It Does

This script iterates over each of the world chunks looking for entities, tile entities, and blocks which are not compatible with Minecraft 1.8 and converts them by changing the ID names, NBT structure, or replacing it with something else that will work most appropriately in the context of Minecraft PvP. Certain objects have been provided with specific conversions, however, the script ties its best to convert incompatible objects that havn't been explicitly defined. You can see which [entities](https://github.com/mitchts/nbt-converter/blob/master/converter/entity.py), [tile entities](https://github.com/mitchts/nbt-converter/blob/master/converter/tileEntity.py), [blocks](https://github.com/mitchts/nbt-converter/blob/master/converter/block.py), and [items](https://github.com/mitchts/nbt-converter/blob/master/converter/item.py) are being converted in their respective files.

## Usage

Open a terminal in the script location and run:

`python converter.py <dir> [options]`

Where `<dir>` is the Minecraft level file directory path, or a root directory for many Minecraft levels (if using the `-r` recursive option)
