from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = Path("data") / "hinos.db"
CSV_PATH = Path("data") / "data_to_load.csv"
OUTPUT_DIR = Path("output") / "slides"
TEMPLATE_DIR = Path("data") / "templates"
