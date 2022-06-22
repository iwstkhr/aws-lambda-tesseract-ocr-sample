import re
from datetime import datetime

import pdf2image
import pytesseract


def lambda_handler(event: dict, context: dict) -> None:
    start = datetime.now()
    result = ''

    images = to_images('run-melos.pdf', 1, 2)
    for image in images:
        result += to_string(image)
    result = normalize(result)

    end = datetime.now()
    duration = end.timestamp() - start.timestamp()

    print('----------------------------------------')
    print(f'Start: {start}')
    print(f'End: {end}')
    print(f'Duration: {int(duration)} seconds')
    print(f'Result: {result}')
    print('----------------------------------------')


def to_images(pdf_path: str, first_page: int = None, last_page: int = None) -> list:
    """ Convert a PDF to a PNG image.

    Args:
        pdf_path (str): PDF path
        first_page (int): First page starting 1 to be converted
        last_page (int): Last page to be converted

    Returns:
        list: List of image data
    """

    print(f'Convert a PDF ({pdf_path}) to a png...')
    images = pdf2image.convert_from_path(
        pdf_path=pdf_path,
        fmt='png',
        first_page=first_page,
        last_page=last_page,
    )
    print(f'A total of converted png images is {len(images)}.')
    return images


def to_string(image) -> str:
    """ OCR an image data.

    Args:
        image: Image data

    Returns:
        str: OCR processed characters
    """

    print(f'Extract characters from an image...')
    return pytesseract.image_to_string(image, lang='jpn')


def normalize(target: str) -> str:
    """ Normalize result text.

    Applying the following:
    - Remove new line.
    - Remove spaces between Japanese characters.

    Args:
        target (str): Target text to be normalized

    Returns:
        str: Normalized text
    """

    result = re.sub('\n', '', target)
    result = re.sub('([あ-んア-ン一-鿐])\s+((?=[あ-んア-ン一-鿐]))', r'\1\2', result)
    return result
