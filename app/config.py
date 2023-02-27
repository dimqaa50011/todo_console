from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_SCHEMA = 'sqlite:////'
DB_NAME = 'db.sqlite3'

SQLALCHEMY_DATABASE_URI = '{}{}'.format(DB_SCHEMA, BASE_DIR / DB_NAME)
