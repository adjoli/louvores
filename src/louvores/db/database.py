from peewee import SqliteDatabase

from louvores.core.config import DB_PATH

db = SqliteDatabase(str(DB_PATH))
