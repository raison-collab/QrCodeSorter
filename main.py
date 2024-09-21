import os
from loguru import logger
from pdf_utils import PDFProcessor


def generate_sorted_pdf(table_pdf_path: str, qr_pdf_path: str, output_pdf_path: str):
    """
    Генерирует отсортированный PDF файл на основе данных из таблицы и QR-кодов.

    :param table_pdf_path: Путь к PDF файлу с таблицей.
    :param qr_pdf_path: Путь к PDF файлу с QR кодами.
    :param output_pdf_path: Путь для сохранения отсортированного PDF.
    :raises FileNotFoundError: Если один из входных файлов не найден.
    :raises ValueError: Если входные файлы не являются PDF.
    """

    if not os.path.exists(table_pdf_path):
        raise FileNotFoundError(f"Файл с таблицей не найден: {table_pdf_path}")
    if not os.path.exists(qr_pdf_path):
        raise FileNotFoundError(f"Файл с QR кодами не найден: {qr_pdf_path}")

    if not table_pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"Файл с таблицей не является PDF: {table_pdf_path}")
    if not qr_pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"Файл с QR кодами не является PDF: {qr_pdf_path}")

    pdf_processor = PDFProcessor(table_pdf_path, qr_pdf_path)

    logger.info(f"Извлечение чисел из PDF с таблицей: {table_pdf_path}")
    table_numbers = pdf_processor.extract_numbers_from_table()

    logger.info(f"Извлечение числовых кодов из PDF с QR кодами: {qr_pdf_path}")
    qr_codes = pdf_processor.extract_numbers_from_qr()

    pdf_processor.create_sorted_pdf(
        output_pdf_path=output_pdf_path,
        table_codes=table_numbers,
        qr_codes=qr_codes
    )

    logger.info(f"Отсортированный PDF сохранён в {output_pdf_path}")


# Генерация отсортированного PDF файла
generate_sorted_pdf(
    'input_table_path.pdf',
    'input_qr_codes_path.pdf',
    'output_sorted_qr_codes_path.pdf'
)
