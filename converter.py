# -*- coding: utf-8 -*-
"""
A tool to convert Minecraft 1.9 to 1.12.2 worlds to a usable state
to be loaded in Minecraft 1.8 by recreating the NBT structures
"""

import os, sys, nbt
from optparse import OptionParser
from nbt.world import WorldFolder
from nbt.nbt import NBTFile
from converter import block as Block
from converter import entity as Entity
from converter import tileEntity as TileEntity
from converter import util as Util

VERSION = "1.1.0"

def save_chunk(region, chunk):
    region.write_chunk(chunk.x, chunk.z, chunk)
    
def save_level(level, world_folder):
    level["Data"].__delitem__("Version")
    level.write_file(os.path.join(world_folder, "level.dat"))

def convert_chunk(chunk, version):
    nbt = chunk["Level"]
    edits = 0
    if (len(nbt["Entities"]) > 0) or (len(nbt["TileEntities"]) > 0):
        for entity in nbt["Entities"]:
            entity, edits = Entity.convert(entity, edits)
        for tile in nbt["TileEntities"]:
            tile, edits = TileEntity.convert(tile, edits)
        if edits > 0:
            print("Made %d modifications in Chunk %s,%s (in world at %s,%s)" % (edits,chunk.x,chunk.z,nbt["xPos"],nbt["zPos"]))
    return chunk, edits

def convert_block(chunk):
    return Block.convert(chunk)

def main(world_folder, options):
    print("Version " + VERSION)
    world = WorldFolder(world_folder)
    if not isinstance(world, nbt.world.AnvilWorldFolder):
        parser.error("%s is not an Anvil world" % (world_folder))
    level = NBTFile(os.path.join(world_folder, "level.dat"))
    version = Util.get_version(level)
    print("\nConverting world located at " + world_folder)
    print("Level saved as Minecraft version " + version)
    if version != "1.8":
        try:
            total_nbt_edits = 0
            total_block_edits = 0
            for region in world.iter_regions():
                for chunk in region.iter_chunks():
                    chunk, nbt_edits = convert_chunk(chunk, version)
                    chunk, block_edits = convert_block(chunk)
                    total_nbt_edits += nbt_edits
                    total_block_edits += block_edits
                    if nbt_edits > 0 or block_edits > 0: save_chunk(region, chunk)
            if (total_nbt_edits > 0) or (total_block_edits > 0):
                if total_nbt_edits > 0: print("%d modifications made to %s" % (total_nbt_edits, world_folder))
                if total_block_edits > 0: print("%d modifications made to block section byte arrays" % (total_block_edits))
                save_level(level, world_folder)
            else:
                print("No NBT data was changed")

        except KeyboardInterrupt:
            return 75
    else:
        print("World is already for Minecraft 1.8")

    return 0

if __name__ == "__main__":
    usage = "usage: %prog <dir> [options]"
    parser = OptionParser(usage=usage)
    #parser.add_option("-n", dest="nested", help="run through nested folders", default=False, action="store_true")
    (options, args) = parser.parse_args()

    if (len(sys.argv) == 1):
        parser.error("No world folder specified")

    world_folder = sys.argv[1]
    world_folder = os.path.normpath(world_folder)
    if (not os.path.exists(world_folder)):
        parser.error("No such folder as " + world_folder)

    sys.exit(main(world_folder, options))
