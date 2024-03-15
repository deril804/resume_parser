import datetime
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import (Docx2txtLoader,
                                                  PyMuPDFLoader, TextLoader)
from transform import count_total_words, ocr_and_save_text
from utils.db import DatabaseConnection

logging.basicConfig(level=logging.INFO)


@dataclass
class ResumePostData:
    file_path: str
    total_num_pages: int
    total_num_words: int
    file_format: str
    extracted_text: str
    inserted_date: str


class AbstractParser(ABC):
    @abstractmethod
    def read(self, dir_path: str) -> list:
        pass

    @abstractmethod
    def extract(self, resumes_path: list) -> list:
        pass

    @abstractmethod
    def load(
        self,
        resume_data: list[ResumePostData],
        db_cursor_context: DatabaseConnection,
    ) -> None:
        pass

    @abstractmethod
    def run(self, dir_path: str) -> None:
        pass


class ResumeParser(AbstractParser):
    def read(self, dir_path: str) -> list:
        logging.info("Reading resume data from directory: %s", dir_path)
        if not dir_path:
            raise ValueError('Resume directory path is empty')

        resumes_path = []
        for resume_file_path in Path(dir_path).glob("**/*"):
            if resume_file_path.is_file():
                resumes_path.append(resume_file_path)
        logging.info("Resumes appended to the list: %s", resumes_path)
        return resumes_path

    def extract(self, resume_paths: list) -> list[ResumePostData]:
        logging.info("Extracting text from resumes...")
        extracted_data = []
        for resume_path in resume_paths:
            logging.info("Extracting text from: %s", resume_path)
            try:
                if resume_path.suffix.lower() == ".pdf":
                    loader = PyMuPDFLoader(str(resume_path))
                elif resume_path.suffix.lower() == ".docx":
                    loader = Docx2txtLoader(str(resume_path))
                elif resume_path.suffix.lower() in (
                    '.png',
                    '.jpg',
                    '.jpeg',
                    '.tiff',
                    '.bmp',
                    '.gif',
                ):
                    temp_file_path = ocr_and_save_text(resume_path)
                    loader = TextLoader(temp_file_path)
                else:
                    logging.warning("Unsupported file format: %s", resume_path)
                    continue

                delimiter = '\n\n\n'
                extract_loader = loader.load()
                extracted_text = delimiter.join(
                    doc.page_content for doc in extract_loader
                )

                total_num_pages = (
                    extract_loader[0].metadata["total_pages"]
                    if "total_pages" in extract_loader[0].metadata
                    else 1
                )
                extracted_data.append(
                    ResumePostData(
                        file_path=str(resume_path),
                        total_num_pages=total_num_pages,
                        total_num_words=count_total_words(extracted_text),
                        file_format=resume_path.suffix.lower(),
                        extracted_text=extracted_text,
                        inserted_date=datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'
                        ),
                    )
                )
            except Exception as e:
                logging.error(
                    "Error extracting text from %s: %s", resume_path, e
                )
                continue

        logging.info("Text extraction completed.")
        return extracted_data

    def load(
        self,
        resume_data: list[ResumePostData],
        db_cursor_context: DatabaseConnection,
    ) -> None:
        logging.info('Loading resume data into database...')
        if not resume_data:
            logging.warning('No resume data to load.')
            return

        with db_cursor_context as cur:
            for extracted_resume in resume_data:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO resume (
                         file_path, total_num_of_pages, total_num_words, file_format, extracted_text, inserted_date 
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        extracted_resume.file_path,
                        extracted_resume.total_num_pages,
                        extracted_resume.total_num_words,
                        extracted_resume.file_format,
                        extracted_resume.extracted_text,
                        extracted_resume.inserted_date,
                    ),
                )
        logging.info('Resume data loaded into the database.')

    def run(
        self, dir_path: str, db_cursor_context: DatabaseConnection
    ) -> None:
        resume_paths = self.read(dir_path)
        extracted_resumes = self.extract(resume_paths)
        self.load(extracted_resumes, db_cursor_context)
