from server import Server
from database import Database

server = Server(True, 3000)
database = Database()

if __name__ == '__main__':
    database.initialize_tables()
    server.start()