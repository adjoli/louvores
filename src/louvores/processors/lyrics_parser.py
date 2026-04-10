import re

from louvores.domain.slide_parts import Estrofe, Refrao, SequenciaHino


def processar_hino(texto: str) -> SequenciaHino:
    # 1. Divide o texto em blocos (separados por linha em branco)
    blocos = re.split(r"\n\s*\n", texto.strip("\n"))

    partes = []
    numero_slide = 1

    for bloco in blocos:
        # Remove linhas completamente vazias (segurança)
        linhas = [l for l in bloco.splitlines() if l.strip()]

        if not linhas:
            continue

        # 2. Verifica se TODAS as linhas do bloco começam com espaço ou tab
        if _eh_refrao(linhas):
            bloco_limpo = "\n".join(l.lstrip() for l in linhas)  # remove indentação
            partes.append(Refrao(bloco_limpo, numero_slide))
        else:  # É estrofe
            partes.append(Estrofe("\n".join(linhas), numero_slide))

        numero_slide += 1

    return SequenciaHino(partes=partes)


def _eh_refrao(linhas: list[str]) -> bool:
    return all(linha.startswith((" ", "\t")) for linha in linhas)
