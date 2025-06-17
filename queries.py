'''Queries for sqlite to mongoDb pipeline'''

# model document
'''
    mongo_document = {
    "name": <VALUE>,
    "level": <VALUE>,
    "exp": <VALUE>,
    "hp": <VALUE>,
    "strength": <VALUE>,
    "intelligence": <VALUE>,
    "dexterity": <VALUE>,
    "wisdom": <VALUE>,
    "items": [
        <ITEM NAME>,
        <ITEM NAME>
    ],
    "weapons" [
        <ITEM NAME>,
        <ITEM NAME>
    ]
    }
'''

GET_CHARACTERS = """
    SELECT * FROM charactercreator_character;
"""

'''return [(character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom)]'''

GET_CHARACTER_INVENTORY = """
    SELECT * FROM charactercreator_character_inventory;
"""

'''returns [(id, character_id, item_id)]'''

GET_ARMORY_ITEMS = """
    SELECT * FROM armory_item;
"""

'''returns [(item_id, name, value, weight)]'''

GET_ARMORY_WEAPONS = """
    SELECT * FROM armory_weapon
"""

'''returns [(item_ptr_id, power)]'''