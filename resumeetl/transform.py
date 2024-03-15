import re
import tempfile
from collections import Counter

import pytesseract
from PIL import Image


def ocr_and_save_text(image_path):
    """
    Performs OCR (Optical Character Recognition) on the image located at the given path,
    extracts text content, and saves it into a temporary file.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Path to the temporary file where the extracted text is saved.
    """
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    with tempfile.NamedTemporaryFile(
        mode='w+', delete=False, suffix='.txt'
    ) as temp_file:
        temp_file.write(extracted_text)
        temp_file_path = temp_file.name
        return temp_file_path


def count_total_words(text):
    # Tokenize the text into words using regular expressions
    words = re.findall(r'\b\w+\b', text.lower())

    # Count the frequency of each word
    word_counts = Counter(words)

    # Sum up the counts of all words
    total_count = sum(word_counts.values())

    return total_count
