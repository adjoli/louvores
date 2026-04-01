import csv
from pathlib import Path
from typing import BinaryIO, List, Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel, select


# -----------------------------------------------------------
class Coletanea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    codigo: str

    hinos: List["Hino"] = Relationship(back_populates="coletanea")


# -----------------------------------------------------------
class Hino(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_coletanea: int = Field(foreign_key="coletanea.id")
    numero: int
    titulo: str
    letra: str = Field(sa_column=Column(Text), default="INSERIR LETRA DO HINO")
    creditos: Optional[str] = Field(default=None)

    coletanea: Coletanea = Relationship(back_populates="hinos")


# -----------------------------------------------------------


def init_db():
    from db import engine

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def load_data():
    coletaneas = [
        Coletanea(nome="Cantor Cristão", codigo="CC"),
        Coletanea(nome="Hinário para o Culto Cristão", codigo="HCC"),
        Coletanea(nome="Voz de Melodia", codigo="VM"),
        Coletanea(nome="Hinos de Louvor", codigo="HL"),
        Coletanea(nome="Corinhos", codigo="COR"),
    ]

    with get_session() as session:
        session.add_all(coletaneas)
        session.commit()


def load_CC_HCC():
    with get_session() as session:
        CC = session.exec(select(Coletanea).where(Coletanea.codigo == "CC")).one()
        HCC = session.exec(select(Coletanea).where(Coletanea.codigo == "HCC")).one()

        with open(Path("CSV") / "CC_HCC.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                match row["coletanea"]:
                    case "CC":
                        session.add(
                            Hino(
                                coletanea=CC,
                                numero=row["codigo"],
                                titulo=row["titulo"],
                                creditos=row["creditos"],
                            )
                        )
                    case "HCC":
                        session.add(
                            Hino(
                                coletanea=HCC,
                                numero=row["codigo"],
                                titulo=row["titulo"],
                                creditos=row["creditos"],
                            )
                        )
            session.commit()


def main():
    init_db()
    load_data()
    load_CC_HCC()


if __name__ == "__main__":
    main()
