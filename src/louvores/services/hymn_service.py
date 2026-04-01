from src.db.database import get_session
from src.db.repository import get_hymn_by_number
from src.ppt.ppt_generator import create_slides
from src.processors.lyrics_parser import parse_lyrics


def generate_hymn_slides(hymn_number: int):
    with get_session() as session:
        hymn = get_hymn_by_number(session, hymn_number)

        if hymn is None:
            raise ValueError(f"Hino {hymn_number} não encontrado")

        parts = parse_lyrics(hymn.letra)
        file_path = create_slides(hymn, parts)

        print(f"Slides gerados em: {file_path}")
