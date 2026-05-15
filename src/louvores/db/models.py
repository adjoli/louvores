from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


class Coletanea(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str
    titulo: str

    hinos: list["Hino"] = Relationship(back_populates="coletanea")


class Hino(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_coletanea: int = Field(foreign_key="coletanea.id")
    numeracao: int | None = Field(default=None)
    titulo: str
    letra: str | None = Field(sa_column=Column(Text), default=None)
    creditos: str | None = Field(default=None)
    revisado: bool = Field(default=False)

    coletanea: Coletanea = Relationship(back_populates="hinos")
