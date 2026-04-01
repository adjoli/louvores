import os
import time

from playwright.sync_api import sync_playwright

BASE_URL = "https://sites.google.com/site/coletaneacantorcristao"
OUTPUT_DIR = "hinos_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def extrair_links(page):
    print("Coletando links dos hinos...")

    # Espera menu lateral carregar
    page.wait_for_selector("a")

    links = page.query_selector_all("a")

    hinos = []

    for link in links:
        href = link.get_attribute("href")
        texto = link.inner_text()

        if href and "/site/coletaneacantorcristao/" in href:
            if texto.strip().startswith(tuple(f"{i:03d}" for i in range(1, 10))):
                num, nome = texto.strip().split(" - ")

                # hinos.append((num, nome, f"{BASE_URL}{href}"))
                hinos.append((num, nome, href))

    # Remove duplicados
    vistos = set()
    resultado = []

    for n, t, h in hinos:
        if h not in vistos:
            vistos.add(h)
            resultado.append((n, t, h))

    print(f"{len(resultado)} links encontrados.")
    return resultado


def extrair_hino(page):
    # page.wait_for_selector("div[role='main']")

    texto = page.inner_text("div[role='main']")

    linhas = [l.strip() for l in texto.splitlines() if l.strip()]

    bloco = []

    for linha in linhas:
        # regra forte: versos têm tamanho e pontuação
        if len(linha) > 20 and ("," in linha or "!" in linha or "." in linha):
            bloco.append(linha)
        elif bloco:
            bloco.append("")  # quebra de estrofe

    titulo = bloco[0] if bloco else "Sem título"
    letra = "\n".join(bloco)

    return titulo, letra


# def extrair_hino(page):
#     page.wait_for_selector("div")

#     # Pega todo o texto visível da página
#     conteudo = page.inner_text("body")

#     linhas = [l.strip() for l in conteudo.splitlines() if l.strip()]

#     # Heurística:
#     # primeira linha relevante = título
#     titulo = linhas[0]

#     # Remove cabeçalho repetido
#     letra = "\n".join(linhas[1:])

#     return titulo, letra


def salvar(numero, titulo, letra):
    nome_limpo = "".join(c for c in titulo if c.isalnum() or c in " -_")
    arquivo = f"{numero:03d} - {nome_limpo}.txt"

    caminho = os.path.join(OUTPUT_DIR, arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"{titulo}\n\n{letra}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        hinos = extrair_links(page)

        # from pprint import pprint

        # pprint(hinos)

        for i, (n, texto, url) in enumerate(hinos, start=1):
            print(f"[{i}] Acessando {url}")

            page.goto(f"{url}")
            time.sleep(1)

            try:
                titulo, letra = extrair_hino(page)
                salvar(i, titulo, letra)
            except Exception as e:
                print(f"Erro no hino {i}: {e}")

        browser.close()


if __name__ == "__main__":
    main()


# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://sites.google.com/site/coletaneacantorcristao")
#     page.get_by_role("link", name="- Antífona").click()
#     page.locator("iframe[name=\"66d5724bbb57cf97_0\"]").content_frame.locator("iframe[name=\"innerFrame\"]").content_frame.locator("#userHtmlFrame").content_frame.get_by_text("A Ti, ó Deus, fiel e bom").click()
#     page.get_by_role("link", name="- Justo És, Senhor").click()
#     page.get_by_role("link", name="- Louvor Ao Senhor").click()
#     page.get_by_role("link", name="- Ao Deus Santo").click()
#     page.get_by_role("link", name="- Presença Divina").click()
#     page.get_by_role("link", name="009 - Santo").click()
#     page.get_by_role("link", name="- Antífona").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
