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
result1 = cursor.execute(query_character_total).fetchall()



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

result2 = cursor.execute(query_unique_subclasses).fetchall()

total_items_query = """
SELECT
	count(DISTINCT item_id)
from
	armory_item
"""
result3 = cursor.execute(total_items_query).fetchall()


total_weapons = """
SELECT
	count(DISTINCT item_ptr_id) as Total_Weapons
from
	armory_weapon
"""

result4 = cursor.execute(total_weapons).fetchall()


items_from_players_query = """
SELECT
	character_id,
	count(item_id)
from
	charactercreator_character_inventory
GROUP BY character_id
LIMIT 20
"""
result4 = cursor.execute(items_from_players_query).fetchall()


average_weapons_query = """

   SELECT AVG(total_weapons)
   FROM (
    SELECT cc.name, COUNT(aw.power) as total_weapons
    FROM charactercreator_character cc
        LEFT JOIN charactercreator_character_inventory cci
            ON cc.character_id=cci.character_id
        LEFT JOIN armory_item ai ON cci.item_id=ai.item_id
        LEFT JOIN armory_weapon aw ON ai.item_id=aw.item_ptr_id
    GROUP BY cc.name)
"""
result = cursor.execute(average_weapons_query).fetchall()
print(f'On average, each character has {result[0][0]:.2f} weapons')

"""
-- On average, how many Items does each Character have?
-- row per character, two columns 1 char name, 2 item count
-- for each character, how many items do they have
-- any characters that don't have any items? 
-- should we include them in our counts?
-- row per char (302 rows)
-- select *
-- from charactercreator_character
-- 898 rows (row per character per item)
-- how many characters in the inventory table??????
-- select count(distinct character_id) as char_count
-- from charactercreator_character_inventory
SELECT AVG(item_count) as avg_item_per_char -- 2.973
FROM (
    -- row per character
    SELECT 
     character_id
     ,count(distinct item_id) as item_count
    FROM charactercreator_character_inventory
    GROUP BY character_id
) subq
-- select 898.0 / 302
SELECT 
  count(id) as row_count
  ,count(distinct character_id) as char_count
  ,count(id) / cast(count(distinct character_id) as float) as avg_item_per_char
FROM charactercreator_character_inventory
"""

"""

SELECT
  c.character_id
  ,inv.*
FROM charactercreator_character c
JOIN charactercreator_character_inventory inv ON inv.character_id = c.character_id
"""