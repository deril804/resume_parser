import argparse
import logging

from utils.db import db_factory


def setup_db_schema():
    """Function to setup the database schema."""
    db = db_factory()
    with db.managed_cursor() as cur:
        logging.info('Creating resume parser table.')
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS resume (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                file_path TEXT NOT NULL,
                total_num_of_pages TEXT,
                total_num_words TEXT,
                file_format TEXT,
                extracted_text TEXT,
                inserted_date TEXT
            );
            """
        )


def teardown_db_schema():
    """Function to teardown the database schema."""
    db = db_factory()
    with db.managed_cursor() as cur:
        logging.info('Dropping resume_extractor table.')
        cur.execute('DROP TABLE IF EXISTS resume_extractor')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--reset-db',
        action='store_true',
        help='Reset your database objects',
    )
    args = parser.parse_args()
    logging.basicConfig(level='INFO')
    if args.reset_db:
        teardown_db_schema()
        setup_db_schema()
