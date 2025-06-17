import sqlite3
import pymongo
from dotenv import load_dotenv
import os
from queries import *

# load .env file
load_dotenv()

# get password and dbname
USER = os.getenv("MONGODB_USER")
PASSWORD = os.getenv("MONGODB_PASSWORD")
DBNAME = os.getenv("MONGODB_NAME")

# open connection to MongoDB
def create_mdb_conn(user, password, dbname, collection_name):
    client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@ds-unit-3-sprint-10-mod.pxenxpb.mongodb.net/{dbname}?retryWrites=true&w=majority&appName=ds-unit-3-sprint-10-module-3")
    # db we want to connect to
    db = client[dbname]
    # create the collection so we can insert into it
    collection = db[collection_name]
    return db

def char_inv_creation(mongo_db, character_inv_list):
    for char_inv in character_inv_list:
        char_inv_doc = {
            'character_id': char_inv[1],
            'item_id': char_inv[2]
        }
        mongo_db.character_inventory.insert_one(char_inv_doc)

def armory_item_creation(mongo_db, armory_item_list):
    for arm_item in armory_item_list:
        arm_item_doc = {
            'item_id': arm_item[0],
            'name': arm_item[1],
            'value': arm_item[2],
            'weight': arm_item[3]
        }
        mongo_db.armory_item.insert_one(arm_item_doc)

def armory_weapon_creation(mongo_db, armory_weapon_list):
    for arm_weapon in armory_weapon_list:
        arm_weapon_doc = {
            'item_ptr_id': arm_weapon[0],
            'power': arm_weapon[1]
        }
        mongo_db.armory_weapon.insert_one(arm_weapon_doc)

# create a document and insert into mongo
def char_doc_creation(mongo_db, character_list):
    for char in character_list:
        #find items and weapons for the character
        char_inventory = list(mongo_db.character_inventory.find({ 'character_id': char[0] }))
        items = []
        weapons = []
        for item in char_inventory:
            item_id = item['item_id']
            item_doc = mongo_db.armory_item.find_one({ 'item_id': item_id })
            name = item_doc['name']
            items.append(name)
            # find weapon
            weapon = mongo_db.armory_weapon.find_one({ 'item_ptr_id': item_id })
            if weapon != None:
                weapons.append(name)
        
        character_doc = {
            'name': char[1],
            'level': char[2],
            'exp': char[3],
            'hp': char[4],
            'strength': char[5],
            'intelligence': char[6],
            'dexterity': char[7],
            'wisdom': char[8],
            'items': items,
            'weapons': weapons
        }
        mongo_db.characters.insert_one(character_doc)

# connect to sqlite
def create_sl_conn(source_db='rpg_db.sqlite3'):
    sl_conn = sqlite3.connect(source_db)
    return sl_conn

# execute a sqlite query
def execute_query(curs, query):
    return curs.execute(query).fetchall()

if __name__ == '__main__':
    # sqlite connection
    sl_conn = create_sl_conn()
    sl_curs = sl_conn.cursor()

    # mongo connections
    char_inv_db = create_mdb_conn(USER, PASSWORD, DBNAME, 'character_inventory')
    char_inventory = execute_query(sl_curs, GET_CHARACTER_INVENTORY)
    char_inv_creation(char_inv_db, char_inventory)

    char_armory_item_db = create_mdb_conn(USER, PASSWORD, DBNAME, 'armory_item')
    char_armory_items = execute_query(sl_curs, GET_ARMORY_ITEMS)
    armory_item_creation(char_armory_item_db, char_armory_items)

    char_armory_weapon_db = create_mdb_conn(USER, PASSWORD, DBNAME, 'armory_weapon')
    char_armory_weapons = execute_query(sl_curs, GET_ARMORY_WEAPONS)
    armory_weapon_creation(char_armory_weapon_db, char_armory_weapons)

    characters_db = create_mdb_conn(USER, PASSWORD, DBNAME, 'characters')
    characters = execute_query(sl_curs, GET_CHARACTERS)
    char_doc_creation(characters_db, characters)