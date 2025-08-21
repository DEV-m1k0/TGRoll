from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///casino.sqlite3", echo=True)

# engine = create_engine(
#     "postgresql+psycopg2://postgres:postgres1234@127.0.0.1:5432/tgroll", echo=True
# )
# engine = create_engine(
#     "postgresql+psycopg2://m1k0:m1k01234@amvera-g3n3ral-cnpg-tgrollpostgresql-rw:5432/tgroll", echo=True
# )

def create_db():
    Base.metadata.create_all(engine)