import db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Producto (Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float)
    categoria = Column(String(200), nullable=False)

    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __repr__(self):
        return "Producto {}: {}, {}, ({})".format(self.id, self.nombre, self.precio, self.contenido)

    def __str__(self):
        return "Producto {}: {}, {}, ({})".format(self.id, self.nombre, self.precio, self.contenido)