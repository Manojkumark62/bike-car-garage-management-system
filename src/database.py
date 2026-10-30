from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = 'mysql+pymysql://root:Password@localhost:3306/databasename'

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()