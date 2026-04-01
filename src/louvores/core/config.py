from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = Path("data") / "hinos.db"
OUTPUT_DIR = Path("output") / "slides"
# DB_PATH = BASE_DIR / "data" / "hinos.db"
# OUTPUT_DIR = BASE_DIR / "output" / "slides"
