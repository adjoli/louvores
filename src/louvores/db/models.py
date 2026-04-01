from typing import List, Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


class Coletanea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    titulo: str

    hinos: List["Hino"] = Relationship(back_populates="coletanea")


class Hino(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_coletanea: int = Field(foreign_key="coletanea.id")
    numeracao: Optional[int] = Field(default=None)
    titulo: str
    letra: str = Field(sa_column=Column(Text), default="INSERIR LETRA DO HINO")
    creditos: Optional[str] = Field(default=None)

    coletanea: Coletanea = Relationship(back_populates="hinos")
