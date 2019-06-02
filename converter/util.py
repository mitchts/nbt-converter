# -*- coding: utf-8 -*-
"""
Simple reusable utilities
"""

import json

POTION_TYPES = ["minecraft:potion", "minecraft:splash_potion", "minecraft:lingering_potion"]

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

def minecraft_to_name(s):
    # minecraft:mob_spawner -> MobSpawner
    return simple_id_to_name(minecraft_to_simple_id(s))

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
    
    text = ""
    # if the sign has multiple colours or specific characters formatted
    # the line will be split up into multiple sections so we need to
    # seperate each of these and treat them by themselves
    sections = []
    json_str = json.loads(str)
    # return empty string is json is None
    if json_str is None:
        return text
    if "extra" in json_str:
        for section in json_str["extra"]:
            sections.append(section)
    else:
        sections.append(json_str)
    
    # go through the line and apply each of the function to the text
    # the order must follow color -> functions -> text otherwise it
    # wont display on the sign properly
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
