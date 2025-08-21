from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///casino.sqlite3", echo=True)



def create_db():
    Base.metadata.create_all(engine)