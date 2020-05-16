# -*- coding: utf-8 -*-
"""
Convert items
"""

from nbt.nbt import TAG_Short
from . import util as Util

def convert_arrow_item(item):
    item["id"].value = "minecraft:arrow"
    return item

def convert_potion_item(item):
    splash = True if item["id"].value in ["minecraft:splash_potion", "minecraft:lingering_potion"] else False
    item["id"].value = "minecraft:potion"
    # if the potion doesn't contain "tag"
    # we can assume it's likely a 1.8 potion already
    if item.__contains__("tag"):
        if item["tag"].__contains__("Potion"):
            damage = Util.potion_name_to_numeric(item["tag"]["Potion"].value, splash)
            item["tag"].__delitem__("Potion")
        elif splash:
            damage = 16447
        else:
            damage = 63
        if item.__contains__("Damage"):
            item["Damage"].value = damage
        else:
            item.__setitem__("Damage", TAG_Short(damage))
    return item

def convert_boat_item(item):
    item["id"].value = "minecraft:boat"
    return item

def convert(item, edits):
    item_id = item["id"].value
    items = {
        "minecraft:tipped_arrow": convert_arrow_item,
        "minecraft:spectral_arrow": convert_arrow_item,
        "minecraft:potion": convert_potion_item,
        "minecraft:splash_potion": convert_potion_item,
        "minecraft:lingering_potion": convert_potion_item,
        "minecraft:spruce_boat": convert_boat_item,
        "minecraft:birch_boat": convert_boat_item,
        "minecraft:jungle_boat": convert_boat_item,
        "minecraft:acacia_boat": convert_boat_item,
        "minecraft:dark_oak_boat": convert_boat_item
    }
    # apply any special conversions if required
    if item_id in items:
        item = items[item_id](item)
        edits += 1

    return item, edits
