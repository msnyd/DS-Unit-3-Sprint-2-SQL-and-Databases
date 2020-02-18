import os
import sqlite3

# construct a path to wherever your database exists
#DB_FILEPATH = "chinook.db"

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "rpg_db.db")
connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
print("CONNECTION:", connection)
cursor = connection.cursor()
print("CURSOR", cursor)
query_character_total =  """
SELECT
	count(distinct character_id) as Total_Players
FROM charactercreator_character
""" 

query_unique_subclasses = """
SELECT
	count(distinct character_ptr_id) as Total_Clerics
FROM
	charactercreator_cleric;

""",
"""
SELECT
	count(distinct character_ptr_id) as Total_Fighters
FROM
	charactercreator_fighter;
""",

"""
SELECT
	count(distinct character_ptr_id) as Total_Mages
FROM
	charactercreator_mage;
""",


"""
SELECT
	count(distinct character_ptr_id) as Total_Thieves
FROM
	charactercreator_thief;
"""

total_items_query = 
"""
SELECT
	count(DISTINCT item_id)
from
	armory_item
"""

total_weapons = 
"""
SELECT
	count(DISTINCT item_ptr_id) as Total_Weapons
from
	armory_weapon
"""
print(total_items_query - total_weapons)

items_from_players_query = 
"""
SELECT
	character_id,
	count(item_id)
from
	charactercreator_character_inventory
GROUP BY character_id
LIMIT 20
"""