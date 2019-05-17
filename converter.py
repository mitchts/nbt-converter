# -*- coding: utf-8 -*-
"""
A tool to convert newer entity and tile entity ids to work with 1.8
Based on https://github.com/twoolie/NBT/blob/master/examples/chest_analysis.py
"""

import os, sys, nbt, json
from nbt.world import WorldFolder
from nbt.region import RegionFile
from nbt.nbt import NBTFile, TAG_String, TAG_Short

VERSION = "1.0.17"
CONTAINERS = ["Chest", "Dispenser", "Dropper", "Cauldron"]

def get_version(level):
    dot = "."
    # if version does not exist in this format, its probably already 1.8 (or earlier)
    if level["Data"].__contains__("Version"):
        version = level["Data"]["Version"]["Name"].value
        # get major version
        version = dot.join(version.split(dot, 2)[:2])
    else:
        version = "1.8"
    return version

def minecraft_to_simple_id(s):
    # minecraft:mob_spawner -> mob_spawner
    if "minecraft:" not in s:
        return s
    else:
        return s.split(":")[1]

def simple_id_to_name(s):
    # mob_spawner -> MobSpawner
    return "".join(map(lambda x:x.capitalize(),s.split("_")))

def formatted_json_to_text(str):
    colors = {
        "black": u"§0",
        "dark_blue": u"§1",
        "dark_green": u"§2",
        "dark_aqua": u"§3",
        "dark_red": u"§4",
        "dark_purple": u"§5",
        "gold": u"§6",
        "gray": u"§7",
        "dark_gray": u"§8",
        "blue": u"§9",
        "green": u"§a",
        "aqua": u"§b",
        "red": u"§c",
        "light_purple": u"§d",
        "yellow": u"§e",
        "white": u"§f"
    }
    functions = {
        "magic": u"§k",
        "bold": u"§l",
        "strikethrough": u"§m",
        "underline": u"§n",
        "italic": u"§o",
        "reset": u"§r"
    }
    
    # if the sign has multiple colours or specific characters formatted
    # the line will be split up into multiple sections so we need to
    # seperate each of these and treat them by themselves
    sections = []
    json_str = json.loads(str)
    if "extra" in json_str:
        for section in json_str["extra"]:
            sections.append(section)
    else:
        sections.append(json_str)
    
    # go through the line and apply each of the function to the text
    # the order must follow color -> functions -> text otherwise it
    # wont display on the sign properly
    text = ""
    for line in sections:
        if "color" in line: text += colors[line.get("color")]
        for function in functions:
            if function in line:
                text += functions[function]
        if "text" in line: text += line.get("text")
        # reset formatting after this section if there are more sections
        if len(sections) > 1: text += functions["reset"]
    return text

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
    if p in potions:
        potion_id = potions[p]
        # convert to splash potion variant
        if splash:
            potion_id = format(potion_id, "b")
            potion_id = int(bin_add(potion_id, "10000000000000"), 2)
    elif splash:
        potion_id = 16447
    else:
        potion_id = 63

    return potion_id

def bin_add(*args):
    return bin(sum(int(x, 2) for x in args))[2:]

def convert_living_entity(entity):
    # get data for main hand as off hand does not exist
    holding_item = entity["HandItems"].tags[0]
    # prepend it to ArmorItems, which will later become Equipment
    # 0 - Holding Item     3 - Chestplate
    # 1 - Boots            4 - Helmet
    # 2 - Leggings
    entity["ArmorItems"].insert(0, holding_item)
    entity["ArmorItems"].name = "Equipment"
    entity.__delitem__("HandItems")
    return entity

def convert_armor_stand(stand, edits):
    stand["id"].value = "ArmorStand"
    stand = convert_living_entity(stand)
    return stand, edits+1

def convert_villager(villager, edits):
    villager["id"].value = "Villager"
    villager = convert_living_entity(villager)
    for trade in villager["Offers"]["Recipes"].tags:
        if trade["buy"]["id"].value in ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]:
            trade["buy"], temp = convert_potion_item(trade["buy"], 0)
        else:
            trade["buy"]["id"].value = minecraft_to_simple_id(trade["buy"]["id"].value)
        if trade["sell"]["id"].value in ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]:
            trade["sell"], temp = convert_potion_item(trade["sell"], 0)
        else:
            trade["sell"]["id"].value = minecraft_to_simple_id(trade["sell"]["id"].value)
    return villager, edits+1

def convert_item_frame(frame, edits):
    frame["id"].value = "ItemFrame"
    if frame["Item"]["id"].value in ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]:
        frame["Item"], temp = convert_potion_item(frame["Item"], 0) 
    return frame, edits+1

def convert_painting(painting, edits):
    painting["id"].value = "Painting"
    return painting, edits+1

def convert_minecart(minecart, edits):
    minecart["id"].value = "MinecartRideable"
    return minecart, edits+1

def convert_minecart_chest(minecart, edits):
    minecart["id"].value = "MinecartChest"
    return minecart, edits+1

def convert_minecart_furnace(minecart, edits):
    minecart["id"].value = "MinecartFurnace"
    return minecart, edits+1

def convert_chest(chest, edits):
    chest["id"].value = "Chest"
    return chest, edits+1

def convert_dispenser(dispenser, edits):
    dispenser["id"].value = "Trap"
    return dispenser, edits+1

def convert_brewing_stand(stand, edits):
    stand["id"].value = "Cauldron"
    return stand, edits+1

def convert_sign(sign, edits):
    sign["id"].value = "Sign"
    sign["Text1"].value = formatted_json_to_text(sign["Text1"].value)
    sign["Text2"].value = formatted_json_to_text(sign["Text2"].value)
    sign["Text3"].value = formatted_json_to_text(sign["Text3"].value)
    sign["Text4"].value = formatted_json_to_text(sign["Text4"].value)
    return sign, edits+1

def convert_skull(skull, edits):
    skull["id"].value = "Skull"
    return skull, edits+1

def convert_banner(banner, edits):
    banner["id"].value = "Banner"
    return banner, edits+1

def convert_beacon(beacon, edits):
    beacon["id"].value = "Beacon"
    return beacon, edits+1

def convert_noteblock(noteblock, edits):
    noteblock["id"].value = "Music"
    return noteblock, edits+1

def convert_jukebox(jukebox, edits):
    jukebox["id"].value = "RecordPlayer"
    return jukebox, edits+1

def convert_spawner(spawner, edits):
    # note: spawners are assumed to be only spawning one type of entity, so if the
    # spawner has many potentials of different types this probably won't work
    spawner["id"].value = "MobSpawner"
    spawner["Delay"].value = 0
    if spawner["SpawnData"].__contains__("id"):
        entity_type = minecraft_to_simple_id(spawner["SpawnData"]["id"].value)
        entity_type = simple_id_to_name(entity_type)
    else:
        entity_type = "Pig"
    # convert entity for next spawn
    # item
    #if spawner["SpawnData"].__contains__("Item"): 
    #    spawner["SpawnData"]["Item"]["id"].value = spawner["SpawnData"]["Item"]["id"].value
    # potion
    if spawner["SpawnData"].__contains__("Potion"):
        spawner["SpawnData"]["Potion"], temp = convert_potion_item(spawner["SpawnData"]["Potion"], 0)
        spawner["SpawnData"]["Potion"]["id"].value = "potion"
    # living entity
    elif spawner["SpawnData"].__contains__("ArmorItems"):
        spawner["SpawnData"] = convert_living_entity(spawner["SpawnData"])
    spawner["SpawnData"].__delitem__("id")
    # convert spawn potentials
    for potential in spawner["SpawnPotentials"].tags:
        # item
        #if potential["Entity"].__contains__("Item"):
        #    spawner["SpawnData"]["Item"]["id"].value = "Item"
        # potion
        if potential["Entity"].__contains__("Potion"):
            potential["Entity"]["Potion"], temp = convert_potion_item(potential["Entity"]["Potion"], 0)
            potential["Entity"]["Potion"]["id"].value = "potion"
            # potion entity name is completely different so we have to manually set it here
            entity_type = "ThrownPotion"
        # living entity
        elif potential["Entity"].__contains__("ArmorItems"):
            potential["Entity"] = convert_living_entity(potential["Entity"])
            entity_type = simple_id_to_name(minecraft_to_simple_id(potential["Entity"]["id"].value))
        potential.__setitem__("Type", TAG_String(entity_type))
        potential["Entity"].__delitem__("id")
        potential["Entity"].name = "Properties"
    spawner.__setitem__("EntityId", TAG_String(entity_type))
    return spawner, edits+1

def convert_arrow_item(item, edits):
    item["id"].value = "minecraft:arrow"
    return item, edits+1

def convert_potion_item(item, edits):
    splash = True if item["id"].value in ["minecraft:splash_potion", "minecraft:lingering_potion"] else False
    item["id"].value = "minecraft:potion"
    if item["tag"]["Potion"]:
        damage = potion_name_to_numeric(item["tag"]["Potion"].value, splash)
        item["tag"].__delitem__("Potion")
    elif splash:
        damage = 16447
    else:
        damage = 63
    if item.__contains__("Damage"):
        item["Damage"].value = damage
    else:
        item.__setitem__("Damage", TAG_Short(damage))
    return item, edits+1

def convert_chunk(chunk, version):
    nbt = chunk["Level"]
    edits = 0
    if (len(nbt["Entities"]) > 0) or (len(nbt["TileEntities"]) > 0):
        for entity in nbt["Entities"]:
            if entity["id"].value == "minecraft:armor_stand": entity, edits = convert_armor_stand(entity, edits)
            if entity["id"].value == "minecraft:villager": entity, edits = convert_villager(entity, edits)
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
            if entity["id"].value == "minecraft:banner": entity, edits = convert_banner(entity, edits)
            if entity["id"].value == "minecraft:beacon": entity, edits = convert_beacon(entity, edits)
            if entity["id"].value == "minecraft:noteblock": entity, edits = convert_noteblock(entity, edits)
            if entity["id"].value == "minecraft:jukebox": entity, edits = convert_jukebox(entity, edits)
            if entity["id"].value in ["minecraft:mob_spawner", "MobSpawner"]: entity, edits = convert_spawner(entity, edits)
            if entity["id"].value in CONTAINERS:
                if entity.__contains__("Items"):
                    for item in entity["Items"]:
                        if item["id"].value in ["minecraft:tipped_arrow", "minecraft:spectral_arrow"]: item, edits = convert_arrow_item(item, edits)
                        if item["id"].value in ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]: item, edits = convert_potion_item(item, edits)
        if edits > 0:
            print("Made %d modifications in Chunk %s,%s (in world at %s,%s)" % (edits,chunk.x,chunk.z,nbt["xPos"],nbt["zPos"]))
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
                    if chunk_edits > 0: save_chunk(region, chunk)
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
