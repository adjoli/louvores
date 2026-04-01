from louvores.core.logging_config import setup_logging
from louvores.db.database import get_session
from louvores.services.import_service import import_data


def main():
    with get_session() as session:
        import_data(session)


if __name__ == "__main__":
    setup_logging()
    main()
