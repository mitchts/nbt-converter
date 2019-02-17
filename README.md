# nbt-converter

A tool to convert maps created in newer Minecraft versions (1.9 to 1.12.2) to be usable in 1.8 for [Stratus Network](https://github.com/StratusNetwork). Uses [twoolie/NBT](https://github.com/twoolie/NBT) for inspecting and editing the Minecraft region files.

This does the absolute minimum to allow Minecraft maps created in newer versions (1.9 to 1.12.2) to be used in a 1.8 server environment by converting the NBT and ids (such as `minecraft:chest` to `Chest`) and so on.

## What Works

#### Entities
- Armor Stands
- Minecarts (and Chest and Furnace variants)

#### Tile Entities
- Chests (and Trapped Chests)
- Brewing Stands
- Dispensers
- Item Frames (not floor and ceiling frames)
- Paintings
- Skulls
- Signs
- (Item) Spawners

#### Items

- Tipped and Spectral Arrows -> Arrows
- Potions
  - Lingering Potions -> Splash Potions

## Usage

`python converter.py '<path to world folder>'`
