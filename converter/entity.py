# -*- coding: utf-8 -*-
"""
Convert entities
"""

from . import item as Item
from . import util as Util

IDS = ["ArmorStand", "Villager", "ItemFrame", "Painting", "MinecartRideable", "MinecartChest", "MinecartFurnace", "PigZombie"]

def convert_armor_stand(stand):
    stand["id"].value = "ArmorStand"
    return stand

def convert_villager(villager):
    villager["id"].value = "Villager"
    if villager.__contains__("Offers"):
        for trade in villager["Offers"]["Recipes"].tags:
            if trade["buy"]["id"].value in Util.POTION_TYPES:
                trade["buy"] = Item.convert_potion_item(trade["buy"])
            else:
                trade["buy"]["id"].value = Util.minecraft_to_simple_id(trade["buy"]["id"].value)
            if trade["sell"]["id"].value in Util.POTION_TYPES:
                trade["sell"] = Item.convert_potion_item(trade["sell"])
            else:
                trade["sell"]["id"].value = Util.minecraft_to_simple_id(trade["sell"]["id"].value)
    return villager

def convert_item_frame(frame):
    frame["id"].value = "ItemFrame"
    if frame.__contains__("Item"):
        if frame["Item"]["id"].value in Util.POTION_TYPES:
            frame["Item"] = Item.convert_potion_item(frame["Item"])
    return frame

def convert_painting(painting):
    painting["id"].value = "Painting"
    return painting

def convert_minecart(minecart):
    minecart["id"].value = "MinecartRideable"
    return minecart

def convert_minecart_chest(minecart):
    minecart["id"].value = "MinecartChest"
    return minecart

def convert_minecart_furnace(minecart):
    minecart["id"].value = "MinecartFurnace"
    return minecart

def convert_zombie_pigman(zombie):
    zombie["id"].value = "PigZombie"
    return zombie

def convert(entity, edits):
    entity_id = entity["id"].value
    entities = {
        "minecraft:armor_stand": convert_armor_stand,
        "minecraft:villager": convert_villager,
        "Villager": convert_villager,
        "minecraft:item_frame": convert_item_frame,
        "minecraft:painting": convert_painting,
        "minecraft:minecart": convert_minecart,
        "minecraft:chest_minecart": convert_minecart_chest,
        "minecraft:furnace_minecart": convert_minecart_furnace,
        "minecraft:zombie_pigman": convert_zombie_pigman
    }
    # convert any equiptment if entity has any
    if entity.__contains__("ArmorItems"):
        holding_item =  entity["HandItems"].tags[0]
        entity["ArmorItems"].insert(0, holding_item)
        entity["ArmorItems"].name = "Equipment"
        entity.__delitem__("HandItems")
    # apply any special conversions if required
    # else attempt to convert minecraft id to old name format
    if entity_id in entities:
        entity = entities[entity_id](entity)
        edits += 1
    else:
        # attempt to correct entity name and record it as an edit
        if entity_id != Util.minecraft_to_name(entity_id):
            entity["id"].value = Util.minecraft_to_name(entity_id)
            edits += 1
        # display warning for entities that may not have been converted correctly
        if entity_id not in IDS:
            print("WARNING: no conversion for entity", entity_id)

    return entity, edits
