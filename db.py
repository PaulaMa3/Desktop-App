from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Producto


engine = create_engine('sqlite:///database/productos.db')

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
