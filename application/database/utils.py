from application.database.database_class import Database

DATABASE = Database('banco.db')


def get_database():
    return DATABASE
