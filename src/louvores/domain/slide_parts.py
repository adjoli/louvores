from dataclasses import dataclass
from enum import Enum


class TipoParte(Enum):
    ESTROFE = "estrofe"
    REFRAO = "refrao"


@dataclass
class ParteHino:
    txt: str
    numero: int

    def rodape(self, num_partes: int) -> str:
        return f"{self.numero}/{num_partes}"

    @property
    def tipo(self) -> TipoParte:
        raise NotImplementedError()


@dataclass
class Estrofe(ParteHino):
    @property
    def tipo(self) -> TipoParte:
        return TipoParte.ESTROFE


@dataclass
class Refrao(ParteHino):
    @property
    def tipo(self) -> TipoParte:
        return TipoParte.REFRAO


@dataclass
class SequenciaHino:
    partes: list[Estrofe | Refrao]
