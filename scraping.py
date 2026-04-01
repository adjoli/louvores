import asyncio
import csv
import re

from playwright.async_api import async_playwright

TOTAL_HINOS = 581
CONCORRENCIA = 8

# Captura nome + (ano-ano)
PADRAO_AUTOR = re.compile(r"([A-Z][A-Za-zÀ-ÿ.\s]+?)\s*\(\d{4}-\d{4}\)")


def limpar_nome(nome: str) -> str:
    return " ".join(nome.split()).strip()


def eh_titulo(nome: str) -> bool:
    """
    Detecta se o texto é um título (geralmente em MAIÚSCULAS)
    """
    letras = [c for c in nome if c.isalpha()]
    if not letras:
        return False

    proporcao_maiuscula = sum(1 for c in letras if c.isupper()) / len(letras)

    return proporcao_maiuscula > 0.9  # ajustável


async def extrair_autores(page, numero_hino: int) -> dict:
    url = f"https://www.revistaebd.com.br/cantor-cristao/{numero_hino}"

    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("article")

        texto = await page.locator("article").inner_text()

        matches = PADRAO_AUTOR.findall(texto)

        autores = []
        for nome in matches:
            nome_limpo = limpar_nome(nome)

            # remove títulos em maiúsculo
            if eh_titulo(nome_limpo):
                continue

            # garante que parece um nome real
            if len(nome_limpo.split()) >= 2:
                autores.append(nome_limpo)

        autores_str = " | ".join(autores)

        return {"numero": numero_hino, "autor": autores_str}

    except Exception:
        return {"numero": numero_hino, "autor": ""}


async def worker(queue, results, browser):
    page = await browser.new_page()

    await page.route(
        "**/*",
        lambda route: route.abort()
        if route.request.resource_type == "image"
        else route.continue_(),
    )

    while not queue.empty():
        numero = await queue.get()

        resultado = await extrair_autores(page, numero)
        results.append(resultado)

        print(f"✔ Hino {numero}")

    await page.close()


async def main():
    queue = asyncio.Queue()
    results = []

    for i in range(1, TOTAL_HINOS + 1):
        await queue.put(i)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [
            asyncio.create_task(worker(queue, results, browser))
            for _ in range(CONCORRENCIA)
        ]

        await asyncio.gather(*tasks)
        await browser.close()

    with open("hinos_autores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["numero", "autor"])
        writer.writeheader()
        writer.writerows(sorted(results, key=lambda x: x["numero"]))

    print("✅ CSV gerado com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
