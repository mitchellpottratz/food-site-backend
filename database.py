from peewee import *
from playhouse.db_url import connect

class Database:

    def __init__(self):
        self.DATABASE = SqliteDatabase('foodsite.sqlite')

    # called when the server starts so the db tables are created
    def initialize_tables(self):
        self.DATABASE.connect()
        self.DATABASE.create_tables([])
        self.DATABASE.close()