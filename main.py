import os
from loguru import logger
from pdf_utils import PDFProcessor


def generate_sorted_pdf(table_pdf_bytes: bytes, qr_pdf_bytes: bytes) -> bytes:
    """
    Генерирует отсортированный PDF файл на основе данных из таблицы и QR-кодов.

    :param table_pdf_bytes: Байтовое представление PDF с таблицей.
    :param qr_pdf_bytes: Байтовое представление PDF с QR кодами.
    :return: Байтовое представление отсортированного PDF.
    """

    pdf_processor = PDFProcessor(table_pdf_bytes, qr_pdf_bytes)

    logger.info(f"Извлечение чисел из PDF с таблицей")
    table_numbers = pdf_processor.extract_numbers_from_table()

    logger.info(f"Извлечение числовых кодов из PDF с QR кодами")
    qr_codes = pdf_processor.extract_numbers_from_qr()

    sorted_pdf_bytes = pdf_processor.create_sorted_pdf(
        table_codes=table_numbers,
        qr_codes=qr_codes
    )

    logger.info(f"Отсортированный PDF сгенерирован")
    return sorted_pdf_bytes


# Генерация отсортированного PDF файла
# Пример использования
with open('Лист подбора Ермак 20.09.24.pdf', 'rb') as table_file, open('Ермак 20.09.24.pdf', 'rb') as qr_file:
    sorted_qr = generate_sorted_pdf(
        table_file.read(),
        qr_file.read(),
    )

with open('sorted.pdf', 'wb') as output_file:
    output_file.write(sorted_qr)
