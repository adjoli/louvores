from pptx import Presentation

from src.core.config import OUTPUT_DIR


def create_slides(hymn, parts):
    prs = Presentation()

    for part in parts:
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        title = slide.shapes.title
        content = slide.placeholders[1]

        title.text = hymn.title
        content.text = "\n".join(part["lines"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = hymn.title.replace(" ", "_")
    file_path = OUTPUT_DIR / f"{hymn.number}_{safe_title}.pptx"
    prs.save(file_path)

    return file_path
