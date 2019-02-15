# nbt-converter

A tool to convert maps created in new Minecraft versions to be usable in 1.8 for [Stratus Network](https://github.com/StratusNetwork). Uses [twoolie/NBT](https://github.com/twoolie/NBT) for inspecting and editing the Minecraft region files.

This does the absolute minimum to allow Minecraft maps created in newer versions to be used in a 1.8 server environment by converting the NBT and ids (such as `minecraft:chest` to `Chest`) and so on.

## What Works

Chests and signs. :)

## Usage

`python converter.py '<path to world folder>'`
