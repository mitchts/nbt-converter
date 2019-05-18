# -*- coding: utf-8 -*-
"""
Convert tile entities
"""

from nbt.nbt import TAG_String
from . import entity as Entity
from . import item as Item
from . import util as Util

CONTAINERS = ["Chest", "Dispenser", "Dropper", "Cauldron"]
IDS = ["Chest", "Trap", "Cauldron", "Sign", "Skull", "Banner", "Beacon", "Music", "RecordPlayer", "MobSpawner"]

def convert_chest(chest):
    chest["id"].value = "Chest"
    return chest

def convert_dispenser(dispenser):
    dispenser["id"].value = "Trap"
    return dispenser

def convert_brewing_stand(stand):
    stand["id"].value = "Cauldron"
    return stand

def convert_sign(sign):
    sign["id"].value = "Sign"
    sign["Text1"].value = Util.formatted_json_to_text(sign["Text1"].value)
    sign["Text2"].value = Util.formatted_json_to_text(sign["Text2"].value)
    sign["Text3"].value = Util.formatted_json_to_text(sign["Text3"].value)
    sign["Text4"].value = Util.formatted_json_to_text(sign["Text4"].value)
    return sign

def convert_skull(skull):
    skull["id"].value = "Skull"
    return skull

def convert_banner(banner):
    banner["id"].value = "Banner"
    return banner

def convert_beacon(beacon):
    beacon["id"].value = "Beacon"
    return beacon

def convert_noteblock(noteblock):
    noteblock["id"].value = "Music"
    return noteblock

def convert_jukebox(jukebox):
    jukebox["id"].value = "RecordPlayer"
    return jukebox

def convert_spawner(spawner):
    # note: spawners are assumed to be only spawning one type of entity, so if the
    # spawner has many potentials of different types this probably won't work
    spawner["id"].value = "MobSpawner"
    spawner["Delay"].value = 0
    if spawner["SpawnData"].__contains__("id"):
        entity_type = Util.minecraft_to_name(spawner["SpawnData"]["id"].value)
    else:
        entity_type = "Pig"
    # convert entity for next spawn
    # item
    #if spawner["SpawnData"].__contains__("Item"): 
    #    spawner["SpawnData"]["Item"]["id"].value = spawner["SpawnData"]["Item"]["id"].value
    # potion
    if spawner["SpawnData"].__contains__("Potion"):
        spawner["SpawnData"]["Potion"] = Item.convert_potion_item(spawner["SpawnData"]["Potion"])
        spawner["SpawnData"]["Potion"]["id"].value = "potion"
    # living entity
    elif spawner["SpawnData"].__contains__("ArmorItems"):
        spawner["SpawnData"] = Entity.convert(spawner["SpawnData"])
    spawner["SpawnData"].__delitem__("id")
    # convert spawn potentials
    for potential in spawner["SpawnPotentials"].tags:
        # item
        #if potential["Entity"].__contains__("Item"):
        #    spawner["SpawnData"]["Item"]["id"].value = "Item"
        # potion
        if potential["Entity"].__contains__("Potion"):
            potential["Entity"]["Potion"] = Item.convert_potion_item(potential["Entity"]["Potion"])
            potential["Entity"]["Potion"]["id"].value = "potion"
            # potion entity name is completely different so we have to manually set it here
            entity_type = "ThrownPotion"
        # living entity
        elif potential["Entity"].__contains__("ArmorItems"):
            potential["Entity"] = Entity.convert(potential["Entity"])
            entity_type = Util.minecraft_to_name(potential["Entity"]["id"].value)
        potential.__setitem__("Type", TAG_String(entity_type))
        potential["Entity"].__delitem__("id")
        potential["Entity"].name = "Properties"
    spawner.__setitem__("EntityId", TAG_String(entity_type))
    return spawner

def convert(tile, edits):
    tiles = {
        "minecraft:chest": convert_chest,
        "minecraft:dispenser": convert_dispenser,
        "minecraft:brewing_stand": convert_brewing_stand,
        "minecraft:sign": convert_sign,
        "minecraft:skull": convert_skull,
        "minecraft:banner": convert_banner,
        "minecraft:beacon": convert_beacon,
        "minecraft:noteblock": convert_noteblock,
        "minecraft:jukebox": convert_jukebox,
        "minecraft:mob_spawner": convert_spawner
    }
    tile_id = tile["id"].value
    # convert the tile entity
    # but check that we can actually convert it first
    if tile_id in tiles:
        tile = tiles[tile_id](tile)
        if tile_id in CONTAINERS:
            if tile.__contains__("Items"):
                for item in tile["Items"]:
                    item, edits = Item.convert(item, edits)
    # show message for tile entities that didn't match
    # but not ones already assumed to be in the right format
    elif tile_id not in IDS:
        print("WARNING: no conversion for tile entity", tile_id)

    return tile, edits+1
