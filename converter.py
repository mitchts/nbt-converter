"""
A tool to convert newer entity and tile entity ids to work with 1.8
Based on https://github.com/twoolie/NBT/blob/master/examples/chest_analysis.py
"""

import os, sys, nbt, json
from nbt.world import WorldFolder
from nbt.region import RegionFile

def convert_chunk(chunk):
    nbt = chunk["Level"]
    edits = 0
    if (len(nbt['Entities']) > 0) or (len(nbt['TileEntities']) > 0):
        """
        for entity in chunk['Entities']:
            if entity["id"].value == "Minecart" and entity["type"].value == 1:
                x,y,z = entity["Pos"]
                x,y,z = x.value,y,value,z.value
                entities.append(Chest("Minecart with chest",(x,y,z)))
        """
        # go through tile entities
        for entity in nbt['TileEntities']:
            # convert chests
            if entity["id"].value == "minecraft:chest":
                entity["id"].value = "Chest"
                edits += 1
            # convert signs
            if entity["id"].value == "minecraft:sign":
                entity["id"].value = "Sign"
                entity["Text1"].value = json.loads(entity["Text1"].value)["text"]
                entity["Text2"].value = json.loads(entity["Text2"].value)["text"]
                entity["Text3"].value = json.loads(entity["Text3"].value)["text"]
                entity["Text4"].value = json.loads(entity["Text4"].value)["text"]
                edits += 1
        # display message if any modifications were made
        if edits > 0:
            print("Made %d modifications in Chunk %s,%s (in world at %s,%s):" % (edits,chunk.x,chunk.z,nbt["xPos"],nbt["zPos"]))
    return chunk, edits

def main(world_folder):
    world = WorldFolder(world_folder)

    try:
        total_edits = 0
        for region in world.iter_regions():
            for chunk in region.iter_chunks():
                chunk_edits = 0
                x,z = chunk.x,chunk.z
                chunk, chunk_edits = convert_chunk(chunk)
                if chunk_edits > 0:
                    region.write_chunk(x, z, chunk)
                    total_edits += 1
        if total_edits == 0:
            print("Nothing to convert in %s" % world_folder)

    except KeyboardInterrupt:
        return 75

    return 0

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print("No world folder specified!")
        sys.exit(64)
    world_folder = sys.argv[1]
    world_folder = os.path.normpath(world_folder)
    if (not os.path.exists(world_folder)):
        print("No such folder as "+world_folder)
        sys.exit(72)
    
    sys.exit(main(world_folder))
