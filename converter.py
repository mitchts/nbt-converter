"""
A tool to convert newer entity and tile entity ids to work with 1.8
Based on https://github.com/twoolie/NBT/blob/master/examples/chest_analysis.py
"""

import os, sys, nbt, json
from nbt.world import WorldFolder
from nbt.region import RegionFile
from nbt.nbt import NBTFile

def get_version(level):
    dot = "."
    # if version doesn"t exist in this format, its probably already 1.8 (or earlier)
    if level["Data"].__contains__("Version"):
        version = level["Data"]["Version"]["Name"].value
        # get major version
        version = dot.join(version.split(dot, 2)[:2])
    else:
        version = "1.8"
    return version

def convert_chest(entity, edits):
    entity["id"].value = "Chest"
    edits += 1

def convert_sign(entity, edits):
    entity["id"].value = "Sign"
    entity["Text1"].value = json.loads(entity["Text1"].value)["text"]
    entity["Text2"].value = json.loads(entity["Text2"].value)["text"]
    entity["Text3"].value = json.loads(entity["Text3"].value)["text"]
    entity["Text4"].value = json.loads(entity["Text4"].value)["text"]
    edits += 1

def convert_chunk(chunk):
    nbt = chunk["Level"]
    edits = 0
    if (len(nbt["Entities"]) > 0) or (len(nbt["TileEntities"]) > 0):
        """
        for entity in chunk["Entities"]:
            if entity["id"].value == "Minecart" and entity["type"].value == 1:
                x,y,z = entity["Pos"]
                x,y,z = x.value,y,value,z.value
                entities.append(Chest("Minecart with chest",(x,y,z)))
        """
        # go through tile entities
        for entity in nbt["TileEntities"]:
            if entity["id"].value == "minecraft:chest":
                convert_chest(entity, edits)
            if entity["id"].value == "minecraft:sign":
                convert_sign(entity, edits)
        # display message if any modifications were made
        if edits > 0:
            print("Made %d modifications in Chunk %s,%s (in world at %s,%s):" % (edits,chunk.x,chunk.z,nbt["xPos"],nbt["zPos"]))
    return chunk, edits

def save_chunk(region, chunk):
    region.write_chunk(chunk.x, chunk.z, chunk)

def main(world_folder):
    world = WorldFolder(world_folder)
    level = NBTFile(os.path.join(world_folder, "level.dat"))
    version = get_version(level)
    try:
        total_edits = 0
        for region in world.iter_regions():
            for chunk in region.iter_chunks():
                chunk, chunk_edits = convert_chunk(chunk)
                total_edits += chunk_edits
                if chunk_edits > 0:
                    save_chunk(region, chunk)
        if total_edits > 0:
            print("%d modifications made to %s" % (total_edits, world_folder))
            # 1.8 doesn't use this
            level["Data"].__delitem__("Version")
            level.write_file(os.path.join(world_folder, "level.dat"))
        else:
            print("Nothing left to convert in" + world_folder)

    except KeyboardInterrupt:
        return 75

    return 0

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        print("No world folder specified!")
        sys.exit(64)
    world_folder = sys.argv[1]
    world_folder = os.path.normpath(world_folder)
    if (not os.path.exists(world_folder)):
        print("No such folder as " + world_folder)
        sys.exit(72)
    
    sys.exit(main(world_folder))
