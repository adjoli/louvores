import re


def processar_hino(texto: str):
    # 1. Divide o texto em blocos (separados por linha em branco)
    blocos = re.split(r"\n\s*\n", texto.strip())

    estrofes = []
    refroes = []

    for bloco in blocos:
        linhas = bloco.splitlines()

        # Remove linhas completamente vazias dentro do bloco (segurança)
        linhas = [l for l in linhas if l.strip()]

        if not linhas:
            continue

        # 2. Verifica se TODAS as linhas começam com espaço ou tab
        if all(re.match(r"^\s+", linha) for linha in linhas):
            # É refrão → remove indentação
            bloco_limpo = "\n".join(l.lstrip() for l in linhas)
            refroes.append(bloco_limpo)
        else:
            # É estrofe
            estrofes.append("\n".join(linhas))

    return {"estrofes": estrofes, "refrao": refroes}
