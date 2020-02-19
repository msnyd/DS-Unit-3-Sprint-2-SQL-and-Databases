import os
from dotenv import load_dotenv
import psycopg2
load_dotenv() #> loads contents of the .env file into the script's environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)
cursor = connection.cursor()
print("CURSOR:", cursor)
# TODO: create a new table


class StorageService():
    def __init__(self):
        self.sqlite_connection = sqlite3.connect(DB_FILEPATH)
        self.sqlite_cursor = self.sqlite_connection.cursor()
        self.pg_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        self.pg_cursor = self.pg_connection.cursor()
    def get_sqlite_characters(self):
        return self.sqlite_connection.execute("SELECT * FROM charactercreator_character;").fetchall()
    def create_pg_characters_table(self):
        create_query = """
        DROP TABLE IF EXISTS characters; -- allows this to be run idempotently, avoids psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "characters_pkey" DETAIL:  Key (character_id)=(1) already exists.
        CREATE TABLE IF NOT EXISTS characters (
            character_id SERIAL PRIMARY KEY,
            name VARCHAR(30),
            level INT,
            exp INT,
            hp INT,
            strength INT,
            intelligence INT,
            dexterity INT,
            wisdom INT
        );
        """
        print(create_query)
        self.pg_cursor.execute(create_query)
        self.pg_connection.commit()
    def insert_pg_characters(self, characters):
        insertion_query = "INSERT INTO characters (character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES %s"
        list_of_tuples = characters
        execute_values(self.pg_cursor, insertion_query, list_of_tuples)
        self.pg_connection.commit()
if __name__ == "__main__":
    service = StorageService()
    #
    # EXTRACT AND TRANSFORM
    #
    characters = service.get_sqlite_characters()
    print(type(characters), len(characters))
    print(characters[0])
    #
    # LOAD
    #
    service.create_pg_characters_table()
    service.insert_pg_characters(characters)