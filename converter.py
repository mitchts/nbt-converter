# -*- coding: utf-8 -*-
"""
A tool to convert Minecraft 1.9 to 1.12.2 worlds to a usable state
to be loaded in Minecraft 1.8 by recreating the NBT structures
"""

import os, sys, nbt
from optparse import OptionParser
from nbt.world import WorldFolder
from nbt.nbt import NBTFile
from conversions import block as Block
from conversions import entity as Entity
from conversions import tileEntity as TileEntity
from conversions import util as Util

VERSION = "1.3.2"

def save_chunk(region, chunk, announce):
    # Discard data version to avoid issues when upgrading the world back
    if chunk.__contains__("DataVersion") and chunk["DataVersion"].value != 0:
        chunk["DataVersion"].value = 0
        if announce:
            print("Discarding chunk version")
    region.write_chunk(chunk.x, chunk.z, chunk)

def save_level(level, world_folder):
    if level["Data"].__contains__("Version"):
        level["Data"].__delitem__("Version")
        level.write_file(os.path.join(world_folder, "level.dat"))

def convert_chunk(chunk):
    nbt = chunk["Level"]
    edits = 0
    entity_edits = 0
    tile_edits = 0
    if (len(nbt["Entities"]) > 0) or (len(nbt["TileEntities"]) > 0):
        print("Inspecting Chunk %+5s: " % (Util.format_chunk(nbt["xPos"], nbt["zPos"])), end="")
        for entity in nbt["Entities"]:
            entity, entity_edits = Entity.convert(entity, entity_edits)
        for tile in nbt["TileEntities"]:
            tile, tile_edits = TileEntity.convert(tile, tile_edits)
        edits = entity_edits + tile_edits
        print("%d modifications made (%d Entities, %d TileEntities)" % (edits, entity_edits, tile_edits))
    return chunk, edits

def convert_block(chunk):
    return Block.convert(chunk)

def disable_keep_inventory(level, world_folder):
    if level["Data"].__contains__("GameRules"):
        if level["Data"]["GameRules"].__contains__("keepInventory"):
            level["Data"]["GameRules"]["keepInventory"].value = "false";
    level.write_file(os.path.join(world_folder, "level.dat"))
    print("keepInventory gamerule has been turned off")

def main(world_folder, options):
    world = WorldFolder(world_folder)

    if not isinstance(world, nbt.world.AnvilWorldFolder):
        print(world_folder + " is not an Anvil world")
        return 0

    level = NBTFile(os.path.join(world_folder, "level.dat"))
    version = Util.get_version(level)

    print("\nLoading level at " + world_folder)
    if version != "1.8" or options.force or options.discard_chunk_version:
        if options.force:
            print("[Forcing level conversion attempt]")
        print("Level saved as Minecraft version " + version)
        try:
            total_nbt_edits = 0
            total_block_edits = 0
            for region in world.iter_regions():
                for chunk in region.iter_chunks():
                    nbt_edits = 0
                    block_edits = 0
                    if not options.discard_chunk_version or options.force:
                        chunk, nbt_edits = convert_chunk(chunk)
                        chunk, block_edits = convert_block(chunk)
                        total_nbt_edits += nbt_edits
                        total_block_edits += block_edits
                    if options.save and (nbt_edits > 0 or block_edits > 0 or options.discard_chunk_version):
                        save_chunk(region, chunk, options.discard_chunk_version)
            if total_nbt_edits > 0 or total_block_edits > 0:
                print("%d modifications made to the level nbt" % (total_nbt_edits))
                print("%d modifications made to block section byte arrays" % (total_block_edits))
                if options.save:
                    save_level(level, world_folder)
                else:
                    print("No modifications saved to level (using -n flag)")
            else:
                print("No level data was changed (nothing to modify)")
        except KeyboardInterrupt:
            return 75
    else:
        print("Level is already saved for Minecraft 1.8 (or older)")

    if options.save and options.disable_keep_inventory:
        disable_keep_inventory(level, world_folder)

    return 0

if __name__ == "__main__":
    print("Version " + VERSION)
    usage = "usage: %prog <dir> [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--recursive",
                      dest="recursive",
                      action="store_true", default=False,
                      help="run through nested folders")
    parser.add_option("-n", "--dry-run",
                      dest="save",
                      action="store_false", default=True,
                      help="do not save modifications made")
    parser.add_option("-f", "--force",
                      dest="force",
                      action="store_true", default=False,
                      help="force the script to run on maps assumed to be 1.8")
    parser.add_option("--disable-keep-inventory",
                      dest="disable_keep_inventory",
                      action="store_true", default=False,
                      help="turn the keepInventory gamerule off")
    parser.add_option("--discard-chunk-version",
                      dest="discard_chunk_version",
                      action="store_true", default=False,
                      help="discards chunk version data - intended for maps already converted still with version data (will not attempt any conversions unless using -f)")
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.error("No world folder specified")

    directory = sys.argv[1]
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        parser.error("No such folder as " + directory)

    if options.recursive == True:
        for dirpath, dirnames, filenames in os.walk(directory):
            if "region" in dirnames and "level.dat" in filenames:
                world = os.path.normpath(dirpath)
                main(world, options)
    else:
        main(directory, options)

    sys.exit(0)
