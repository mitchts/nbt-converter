# -*- coding: utf-8 -*-
"""
Convert entities
"""

from . import item as Item
from . import util as Util

IDS = ["ArmorStand", "Villager", "ItemFrame", "Painting", "MinecartRideable", "MinecartChest", "MinecartFurnace"]

def convert_armor_stand(stand):
    stand["id"].value = "ArmorStand"
    return stand

def convert_villager(villager):
    villager["id"].value = "Villager"
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
    if frame["Item"]["id"].value in Util.POTION_TYPES:
        frame["Item"] = Util.convert_potion_item(frame["Item"]) 
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

def convert(entity, edits):
    entities = {
        "minecraft:armor_stand": convert_armor_stand,
        "minecraft:villager": convert_villager,
        "minecraft:item_frame": convert_item_frame,
        "minecraft:painting": convert_painting,
        "minecraft:minecart": convert_minecart,
        "minecraft:chest_minecart": convert_minecart_chest,
        "minecraft:furnace_minecart": convert_minecart_furnace
    }
    entity_id = entity["id"].value
    # convert the entity
    # but check that we can actually convert it first
    if entity_id in entities:
        if entity.__contains__("ArmorItems"):
            # convert any equipment
            holding_item =  entity["HandItems"].tags[0]
            entity["ArmorItems"].insert(0, holding_item)
            entity["ArmorItems"].name = "Equipment"
            entity.__delitem__("HandItems")
        entity = entities[entity_id](entity)
        edits += 1
    # show message for entities that didn't match
    # but not ones already assumed to be in the right format
    elif entity_id not in IDS:
        print("WARNING: no conversion for entity", entity_id)

    return entity, edits
