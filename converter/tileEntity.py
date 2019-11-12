# -*- coding: utf-8 -*-
"""
Convert tile entities
"""

from nbt.nbt import TAG_String
from . import entity as Entity
from . import item as Item
from . import util as Util

CONTAINERS = ["Chest", "Furnace", "Dispenser", "Dropper", "Cauldron"]
IDS = ["Chest", "Furnace", "Trap", "Cauldron", "Sign", "Skull", "Banner", "Beacon", "Music", "RecordPlayer", "MobSpawner"]

def convert_container_contents(tile):
    if tile.__contains__("Items"):
        for item in tile["Items"]:
            item, temp = Item.convert(item, 0)
    return tile

def convert_chest(chest):
    chest["id"].value = "Chest"
    chest = convert_container_contents(chest)
    return chest

def convert_shulker_box(box):
    box["id"].value = "Chest"
    box = convert_container_contents(box)
    return box

def convert_furnace(furnace):
    furnace["id"].value = "Furnace"
    furnace = convert_container_contents(furnace)
    return furnace

def convert_dispenser(dispenser):
    dispenser["id"].value = "Trap"
    dispenser = convert_container_contents(dispenser)
    return dispenser

def convert_dropper(dropper):
    dropper["id"].value = "Dropper"
    dropper = convert_container_contents(dropper)
    return dropper

def convert_brewing_stand(stand):
    stand["id"].value = "Cauldron"
    stand = convert_container_contents(stand)
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
        entity_type = Util.convert_entity_id(spawner["SpawnData"]["id"].value)
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
        spawner["SpawnData"], temp = Entity.convert(spawner["SpawnData"], 0)
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
            potential["Entity"], temp = Entity.convert(potential["Entity"], 0)
            entity_type = Util.minecraft_to_name(potential["Entity"]["id"].value)
        potential.__setitem__("Type", TAG_String(entity_type))
        potential["Entity"].__delitem__("id")
        potential["Entity"].name = "Properties"
    spawner.__setitem__("EntityId", TAG_String(entity_type))
    return spawner

def convert(tile, edits):
    tile_id = tile["id"].value
    tiles = {
        "minecraft:chest": convert_chest,
        "minecraft:shulker_box": convert_shulker_box,
        "minecraft:furnace": convert_furnace,
        "minecraft:dispenser": convert_dispenser,
        "minecraft:dropper": convert_dropper,
        "minecraft:brewing_stand": convert_brewing_stand,
        "minecraft:sign": convert_sign,
        "minecraft:skull": convert_skull,
        "minecraft:banner": convert_banner,
        "minecraft:beacon": convert_beacon,
        "minecraft:noteblock": convert_noteblock,
        "minecraft:jukebox": convert_jukebox,
        "minecraft:mob_spawner": convert_spawner
    }
    # apply any special conversions if required
    # else attempt to convert minecraft id to old name format
    if tile_id in tiles:
        tile = tiles[tile_id](tile)
        edits += 1
    else:
        # attempt to correct tile entity name and record it as an edit
        if tile_id != Util.minecraft_to_name(tile_id):
            tile["id"].value = Util.minecraft_to_name(tile_id)
            edits += 1
        # display warning for entities that may not have been converted correctly
        if tile_id not in IDS:
            print("WARNING: no conversion for tile entity", tile_id)

    return tile, edits
