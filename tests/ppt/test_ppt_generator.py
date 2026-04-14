from louvores.domain.slide_parts import Estrofe, Refrao, SequenciaHino
from louvores.ppt.ppt_generator import create_slides


# --------------------------------------------
def test_cria_apresentacao(coletanea_factory, hino_factory, template_path):
    hino = hino_factory()
    hino.coletanea = coletanea_factory()

    sequencia = SequenciaHino(
        partes=[
            Estrofe("Linha 1\nLinha 2", 1),
            Refrao("Refrao 1\nRefrao 2", 2),
        ]
    )

    prs = create_slides(hino, sequencia, template_path)

    assert len(prs.slides) == 3


# --------------------------------------------
def test_conteudo_do_slide(coletanea_factory, hino_factory, template_path):
    hino = hino_factory()
    hino.coletanea = coletanea_factory()

    sequencia = SequenciaHino(
        partes=[
            Estrofe("Linha A", 1),
        ]
    )

    prs = create_slides(hino, sequencia, template_path)

    slide = prs.slides[1]

    assert slide.shapes.title.text == "Hino PADRÃO"
    assert "Linha A" in slide.placeholders[1].text


# --------------------------------------------
def test_rodape(coletanea_factory, hino_factory, template_path):
    hino = hino_factory()
    hino.coletanea = coletanea_factory()

    sequencia = SequenciaHino(
        partes=[
            Estrofe("A", 1),
            Estrofe("B", 2),
            Estrofe("C", 3),
        ]
    )

    prs = create_slides(hino, sequencia, template_path)

    slide1 = prs.slides[1]
    slide2 = prs.slides[2]
    slide3 = prs.slides[3]

    assert "1/3" in slide1.shapes[2].text
    assert "2/3" in slide2.shapes[2].text
    assert "3/3" in slide3.shapes[2].text
