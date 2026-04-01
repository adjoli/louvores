from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "hinos.db"
OUTPUT_DIR = BASE_DIR / "output" / "slides"
