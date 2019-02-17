"""
A tool to convert newer entity and tile entity ids to work with 1.8
Based on https://github.com/twoolie/NBT/blob/master/examples/chest_analysis.py
"""

import os, sys, nbt, json
from nbt.world import WorldFolder
from nbt.region import RegionFile
from nbt.nbt import NBTFile, TAG_String

VERSION = "1.0.6"
CONTAINERS = ["Chest", "Dispenser", "Dropper", "Cauldron"]

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

def minecraft_to_simple_id(s):
    # minecraft:mob_spawner -> mob_spawner
    return s.split(':')[1]

def simple_id_to_name(s):
    # mob_spawner -> MobSpawner
    return ''.join(map(lambda x:x.capitalize(),s.split('_')))

def potion_name_to_numeric(p, splash = False):
    potions = {
        "regeneration": 8193,
        "strong_regeneration": 8225,
        "long_regeneration": 8257,
        "swiftness": 8194,
        "strong_swiftness": 8226,
        "long_swiftness": 8258,
        "fire_resistance": 8195,
        "long_fire_resistance": 8259,
        "poison": 8196,
        "strong_poison": 8228,
        "long_poison": 8260,
        "healing": 8197,
        "strong_healing": 8229,
        "night_vision": 8198,
        "long_night_vision": 8262,
        "weakness": 8200,
        "long_weakness": 8264,
        "strength": 8201,
        "strong_strength": 8233,
        "long_strength": 8265,
        "slowness": 8202,
        "strong_slowness": 8234,
        "long_slowness": 8266,
        "leaping": 8203,
        "strong_leaping": 8236,
        "long_leaping": 8267,
        "harming": 8204,
        "strong_harming": 8268,
        "water_breathing": 8205,
        "long_water_breathing": 8269,
        "invisibility": 8206,
        "long_invisibility": 8270
    }

    # check that potion exists in 1.8 else use a stinky potion
    # and hope it has some other custom effects
    p = minecraft_to_simple_id(p)
    if potions[p]:
        potion_id = potions[p]
        # turn off the 13th and turn on 14th to
        # make it a splash potion variant
        if splash:
            potion_id = format(potion_id, 'b')
            potion_id = int(bin_add(potion_id, '10000000000000'), 2)
    elif splash:
        potion_id = 16447
    else:
        potion_id = 63

    return potion_id

def bin_add(*args):
    return bin(sum(int(x, 2) for x in args))[2:]

def convert_armor_stand(entity, edits):
    entity["id"].value = "ArmorStand"
    # get data for main hand as off hand doesn't exist
    holding_item = entity["HandItems"].tags[0]
    # prepend it to ArmorItems, which will later become Equipment
    # 0 - Holding Item     3 - Chestplate
    # 1 - Boots            4 - Helmet
    # 2 - Leggings
    entity["ArmorItems"].insert(0, holding_item)
    entity["ArmorItems"].name = "Equipment"
    entity.__delitem__("HandItems")
    return entity, edits+1

def convert_item_frame(entity, edits):
    entity["id"].value = "ItemFrame"
    return entity, edits+1

def convert_painting(entity, edits):
    entity["id"].value = "Painting"
    return entity, edits+1

def convert_minecart(entity, edits):
    entity["id"].value = "MinecartRideable"
    return entity, edits+1

def convert_minecart_chest(entity, edits):
    entity["id"].value = "MinecartChest"
    return entity, edits+1

def convert_minecart_furnace(entity, edits):
    entity["id"].value = "MinecartFurnace"
    return entity, edits+1

def convert_chest(entity, edits):
    entity["id"].value = "Chest"
    return entity, edits+1

def convert_dispenser(entity, edits):
    entity["id"].value = "Trap"
    return entity, edits+1

def convert_brewing_stand(entity, edits):
    entity["id"].value = "Cauldron"
    return entity, edits+1

def convert_sign(entity, edits):
    entity["id"].value = "Sign"
    entity["Text1"].value = json.loads(entity["Text1"].value)["text"]
    entity["Text2"].value = json.loads(entity["Text2"].value)["text"]
    entity["Text3"].value = json.loads(entity["Text3"].value)["text"]
    entity["Text4"].value = json.loads(entity["Text4"].value)["text"]
    return entity, edits+1

def convert_skull(entity, edits):
    entity["id"].value = "Skull"
    return entity, edits+1

def convert_spawner(entity, edits):
    entity["id"].value = "MobSpawner"
    entity["Delay"].value = 0
    # default to item unless otherwise set somewhere else
    entity_type = "Item"
    # convert data for next spawn
    entity["SpawnData"].__delitem__("id")
    if entity["SpawnData"].__contains__("Item"):
        entity["SpawnData"]["Item"]["id"].value = minecraft_to_simple_id(entity["SpawnData"]["Item"]["id"].value)
    # convert spawn potentials
    for potential in entity["SpawnPotentials"].tags:
        # entity type
        potential.__setitem__("Type", TAG_String(minecraft_to_simple_id(potential["Entity"]["id"].value).capitalize()))
        potential["Entity"].__delitem__("id")
        # item conversion
        if potential["Entity"].__contains__("Item"):
            potential["Entity"]["Item"]["id"].value = minecraft_to_simple_id(potential["Entity"]["Item"]["id"].value)
        # rename 'Entity' to 'Properties'
        potential["Entity"].name = "Properties"
    entity.__setitem__("EntityId", TAG_String(entity_type))
    return entity, edits+1

def convert_arrow_item(item, edits):
    item["id"].value = "minecraft:arrow"
    return item, edits+1

def convert_potion_item(item, edits):
    splash = True if item["id"].value in ["minecraft:splash_potion", "minecraft:lingering_potion"] else False
    item["id"].value = "minecraft:potion"
    if item["tag"]["Potion"]:
        item["Damage"].value = potion_name_to_numeric(item["tag"]["Potion"].value, splash)
        item.__delitem__("tag")
    elif splash:
        item["Damage"].value = 16447
    else:
        item["Damage"].value = 63
    return item, edits+1

def convert_chunk(chunk, version):
    nbt = chunk["Level"]
    edits = 0
    if (len(nbt["Entities"]) > 0) or (len(nbt["TileEntities"]) > 0):
        for entity in nbt["Entities"]:
            if entity["id"].value == "minecraft:armor_stand": entity, edits = convert_armor_stand(entity, edits)
            if entity["id"].value == "minecraft:item_frame": entity, edits = convert_item_frame(entity, edits)
            if entity["id"].value == "minecraft:painting": entity, edits = convert_painting(entity, edits)
            if entity["id"].value == "minecraft:minecart": entity, edits = convert_minecart(entity, edits)
            if entity["id"].value == "minecraft:chest_minecart": entity, edits = convert_minecart_chest(entity, edits)
            if entity["id"].value == "minecraft:furnace_minecart": entity, edits = convert_minecart_furnace(entity, edits)
        for entity in nbt["TileEntities"]:
            if entity["id"].value == "minecraft:chest": entity, edits = convert_chest(entity, edits)
            if entity["id"].value == "minecraft:dispenser": entity, edits = convert_dispenser(entity, edits)
            if entity["id"].value == "minecraft:brewing_stand": entity, edits = convert_brewing_stand(entity, edits)
            if entity["id"].value == "minecraft:sign": entity, edits = convert_sign(entity, edits)
            if entity["id"].value == "minecraft:skull": entity, edits = convert_skull(entity, edits)
            if entity["id"].value in ["minecraft:mob_spawner", "MobSpawner"]: entity, edits = convert_spawner(entity, edits)
            if entity["id"].value in CONTAINERS:
                for item in entity["Items"]:
                    if item["id"].value in ["minecraft:tipped_arrow", "minecraft:spectral_arrow"]: item, edits = convert_arrow_item(item, edits)
                    if item["id"].value in ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]: item, edits = convert_potion_item(item, edits)
        if edits > 0:
            print("Made %d modifications in Chunk %s,%s (in world at %s,%s):" % (edits,chunk.x,chunk.z,nbt["xPos"],nbt["zPos"]))
    return chunk, edits

def save_chunk(region, chunk):
    region.write_chunk(chunk.x, chunk.z, chunk)
    
def save_level(level, world_folder):
    level["Data"].__delitem__("Version")
    level.write_file(os.path.join(world_folder, "level.dat"))

def main(world_folder):
    print("Version " + VERSION)
    world = WorldFolder(world_folder)
    level = NBTFile(os.path.join(world_folder, "level.dat"))
    version = get_version(level)
    print("\nConverting world located at " + world_folder)
    print("Level saved as Minecraft version " + version)
    if version != "1.8":
        try:
            total_edits = 0
            for region in world.iter_regions():
                for chunk in region.iter_chunks():
                    chunk, chunk_edits = convert_chunk(chunk, version)
                    total_edits += chunk_edits
                    if chunk_edits > 0:
                        save_chunk(region, chunk)
            if total_edits > 0:
                print("%d modifications made to %s" % (total_edits, world_folder))
                save_level(level, world_folder)
            else:
                print("No NBT data was changed")

        except KeyboardInterrupt:
            return 75
    else:
        print("World is already for Minecraft 1.8")

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
