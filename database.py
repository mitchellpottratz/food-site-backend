from peewee import *

class Database:

    def __init__(self, db_tables):
        print('----- In Database constructor -----')
        self.DATABASE = SqliteDatabase('foodsite.sqlite')
        self.db_tables = db_tables

    # called when the server starts so the db tables are created
    def initialize_tables(self):
        print('----- Initializing database tables -----')
        self.DATABASE.connect()
        self.DATABASE.create_tables(self.db_tables)
        self.DATABASE.close()