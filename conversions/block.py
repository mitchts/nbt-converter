# -*- coding: utf-8 -*-
"""
Convert Minecraft 1.9 to 1.12.2 blocks to similar blocks
in appearance or function as a Minecraft 1.8 replacement
"""

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
        198: 50, #end rod -> torch
        199: 168, #chrous plant -> prismarine
        200: 169, #chrous flower -> sea lantern
        201: 155, #purpur block -> quartz block
        202: 155, #purpur pillar -> quartz block
        203: 156, #purpur stairs -> quartz stairs
        204: 43, #purpur double slab -> double quartz slab
        205: 44, #purpur slab -> quartz slab
        206: 121, #end stone bricks -> end stone
        208: 3, #path -> dirt
        213: 87, #magma block -> netherrack
        214: 45, #nether wart block -> brick block
        215: 112, #red nether brick -> nether brick
        216: 159, #bone block -> stained clay
        218: 23, #observer -> dispenser
        219: 54, #white shulker box -> chest
        220: 54, #orange shulker box -> chest
        221: 54, #magenta shulker box -> chest
        222: 54, #light blue shulker box -> chest
        223: 54, #yellow shulker box -> chest
        224: 54, #lime shulker box -> chest
        225: 54, #pink shulker box -> chest
        226: 54, #grey shulker box -> chest
        227: 54, #light grey shulker box -> chest
        228: 54, #cyan shulker box -> chest
        229: 54, #purple shulker box -> chest
        230: 54, #blue shulker box -> chest
        231: 54, #brown shulker box -> chest
        232: 54, #green shulker box -> chest
        233: 54, #red shulker box -> chest
        234: 54, #black shulker box -> chest
        235: 159, #white glazed terracotta -> stained clay
        236: 159, #orange glazed terracotta -> stained clay
        237: 159, #magenta glazed terracotta -> stained clay
        238: 159, #light blue glazed terracotta -> stained clay
        239: 159, #yellow glazed terracotta -> stained clay
        240: 159, #lime glazed terracotta -> stained clay
        241: 159, #pink glazed terracotta -> stained clay
        242: 159, #grey glazed terracotta -> stained clay
        243: 159, #light grey glazed terracotta -> stained clay
        244: 159, #cyan glazed terracotta -> stained clay
        245: 159, #purple glazed terracotta -> stained clay
        246: 159, #blue glazed terracotta -> stained clay
        247: 159, #brown glazed terracotta -> stained clay
        248: 159, #green glazed terracotta -> stained clay
        249: 159, #red glazed terracotta -> stained clay
        250: 159, #black glazed terracotta -> stained clay
        251: 159, #concrete -> stained clay
        252: 159, #concrete powder -> stained clay
    }
    modified = 0
    for s in chunk['Level']['Sections']:
        # in some cases the section will not have any blocks,
        # however it is unclear when or how this happens so
        # putting a simple check here for when it does occur.
        if not s.__contains__('Blocks'):
            continue

        block_ids, indexes = fetch_section_blocks(s)
        for i, b in enumerate(block_ids):
            if b in replacements:
                block_ids[i] = replacements[b]
                modified += 1
        s['Blocks'].value = reconstruct_data(block_ids, indexes)

    return chunk, modified
    
