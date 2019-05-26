# -*- coding: utf-8 -*-
"""
Convert Minecraft 1.9 to 1.12.2 blocks to similar blocks
in appearance as a Minecraft 1.8 replacement
"""

CHUNK_HEIGHT = 254
CHUNK_LENGTH = 16

def get_block_replacement(b):
    replacements = {
        198: "", #end rod
        199: "", #chrous plant
        200: "", #chrous flower
        201: "", #purpur block
        202: "", #purpur pillar
        203: "", #purpur stairs
        304: "", #purpur double slab
        205: "", #purpur slab
        206: "", #end stone bricks
        213: "", #magme block
        214: "", #nether wart block
        215: "", #red nether brick
        216: "", #bone block
        218: "", #observer
        219: "", #white shulker box
        220: "", #orange
        221: "", #magenta
        222: "", #light blue
        223: "", #yellow
        224: "", #lime
        225: "", #pink
        226: "", #grey
        227: "", #light grey
        228: "", #cyan
        229: "", #purple
        230: "", #blue
        231: "", #brown
        232: "", #green
        233: "", #red
        234: "", #black
        235: "", #white glazed terracotta
        236: "", 
        237: "",
        238: "",
        239: "",
        240: "",
        241: "",
        242: "",
        243: "",
        244: "",
        245: "",
        246: "",
        257: "",
        258: "",
        259: "",
        260: "",
        195: "",
        "White Concrete": "", #white concrete
        "Orange Concrete": "",
        "Magenta Concrete": "",
        "Light Concrete": "",
        "Yellow Concrete": "",
        "Lime Concrete": "",
        "Pink Concrete": "",
        "Grey Concrete": "",
        "Light Concrete": "",
        "Cyan Concrete": "",
        "Purple Concrete": "",
        "Blue Concrete": "",
        "Brown Concrete": "",
        "Green Concrete": "",
        "Red Concrete": "",
        "Black Concrete": "",
        "White Concrete Powder": "", #white concrete powder
        "Orange Concrete Powder": "",
        "Magenta Concrete Powder": "",
        "Light Concrete Powder": "",
        "Yellow Concrete Powder": "",
        "Lime Concrete Powder": "",
        "Pink Concrete Powder": "",
        "Grey Concrete Powder": "",
        "Light Concrete Powder": "",
        "Cyan Concrete Powder": "",
        "Purple Concrete Powder": "",
        "Blue Concrete Powder": "",
        "Brown Concrete Powder": "",
        "Green Concrete Powder": "",
        "Red Concrete Powder": "",
        "Black Concrete Powser": "",
        "White Bed": "", #white bed
        "Orange Bed": "",
        "Magenta Bed": "",
        "Light Bed": "",
        "Yellow Bed": "",
        "Lime Bed": "",
        "Pink Bed": "",
        "Grey Bed": "",
        "Light Bed": "",
        "Cyan Bed": "",
        "Purple Bed": "",
        "Blue Bed": "",
        "Brown Bed": "",
        "Green Bed": "",
        "Red Bed": "",
        "Black Bed": ""
    }
    
def fetch_section_blocks(s):
    ids = []
    indexes = []
    bids = []

    for bid in s['Blocks'].value:
        try:
            i = bids.index(bid)
        except ValueError:
            bids.append(bid)
            i = len(bids) - 1
        indexes.append(i)

    for bid in bids:
        ids.append(bid)

    return ids, indexes
    
def reconstruct_data(ids, indexes):
    values = []
    for index in indexes:
        values.append(ids[index])
    return bytearray(values)

def convert(chunk):
    replacements = {
        198: "", #end rod
        199: "", #chrous plant
        200: "", #chrous flower
        201: "", #purpur block
        202: "", #purpur pillar
        203: "", #purpur stairs
        304: "", #purpur double slab
        205: "", #purpur slab
        206: "", #end stone bricks
        213: "", #magme block
        214: "", #nether wart block
        215: "", #red nether brick
        216: "", #bone block
        218: "", #observer
        219: "", #white shulker box
        220: "", #orange shulker box
        221: "", #magenta shulker box
        222: "", #light blue shulker box
        223: "", #yellow shulker box
        224: "", #lime shulker box
        225: "", #pink shulker box
        226: "", #grey shulker box
        227: "", #light grey shulker box
        228: "", #cyan shulker box
        229: "", #purple shulker box
        230: "", #blue shulker box
        231: "", #brown shulker box
        232: "", #green shulker box
        233: "", #red shulker box
        234: "", #black shulker box
        235: "", #white glazed terracotta
        236: "", 
        237: "",
        238: "",
        239: "",
        240: "",
        241: "",
        242: "",
        243: "",
        244: "",
        245: "",
        246: "",
        257: "",
        258: "",
        259: "",
        260: "",
        195: "",
        "White Concrete": "", #white concrete
        "Orange Concrete": "",
        "Magenta Concrete": "",
        "Light Concrete": "",
        "Yellow Concrete": "",
        "Lime Concrete": "",
        "Pink Concrete": "",
        "Grey Concrete": "",
        "Light Concrete": "",
        "Cyan Concrete": "",
        "Purple Concrete": "",
        "Blue Concrete": "",
        "Brown Concrete": "",
        "Green Concrete": "",
        "Red Concrete": "",
        "Black Concrete": "",
        "White Concrete Powder": "", #white concrete powder
        "Orange Concrete Powder": "",
        "Magenta Concrete Powder": "",
        "Light Concrete Powder": "",
        "Yellow Concrete Powder": "",
        "Lime Concrete Powder": "",
        "Pink Concrete Powder": "",
        "Grey Concrete Powder": "",
        "Light Concrete Powder": "",
        "Cyan Concrete Powder": "",
        "Purple Concrete Powder": "",
        "Blue Concrete Powder": "",
        "Brown Concrete Powder": "",
        "Green Concrete Powder": "",
        "Red Concrete Powder": "",
        "Black Concrete Powser": "",
    }
    ids = {
        8: 1,
        2: 7,
        3: 103
    }
    modified = 0
    for s in chunk['Level']['Sections']:
        block_ids, indexes = fetch_section_blocks(s)
        for i, b in enumerate(block_ids):
            if b in ids:
                ref = ids[b]
                print(block_ids[i], "->", ref)
                block_ids[i] = ids[b]
                print(block_ids[i], "=", ref)
                modified += 1
            print(block_ids)
        s['Blocks'].value = reconstruct_data(block_ids, indexes)
        print(s['Blocks'])
            
    #return chunk.set_blocks(ids, False)
    return chunk, modified
                #block_id = chunk.get_block_data(x, y, z)
                #if block_id not in [0]:
                #    print(block_id)
    
