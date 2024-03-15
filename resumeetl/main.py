import argparse
import logging
from pathlib import Path

from resume_parser import ResumeParser
from utils.db import db_factory


def main(dir_path: str):
    logging.info(f'Starting extraction from {dir_path}')
    logging.info("Initializing the db factory")
    db = db_factory()
    RP_OBJ = ResumeParser()
    RP_OBJ.run(dir_path=dir_path, db_cursor_context=db.managed_cursor())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dirpath',
        default='data/resume',
        type=str,
        help='Indicates which path to read',
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="basic.log",
        force=True,
        filemode="w"
    )
    main(dir_path=Path(args.dirpath))
