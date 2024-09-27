import io
import fitz
import pdfplumber
from loguru import logger
import re


class PDFProcessor:
    def __init__(self, pdf_table_bytes: bytes, pdf_qrs_bytes: bytes):
        """
        Инициализация процессора для работы с PDF.

        :param pdf_table_bytes: PDF файл с таблицей в виде байтов.
        :param pdf_qrs_bytes: PDF файл с QR кодами в виде байтов.
        """
        self.pdf_table_bytes = pdf_table_bytes
        self.pdf_qrs_bytes = pdf_qrs_bytes
        self.qr_doc = fitz.open(stream=self.pdf_qrs_bytes, filetype="pdf")

    def extract_numbers_from_qr(self) -> list[tuple[int, str]]:
        """
        Извлекает числа из QR кодов в PDF.

        :return: Список кортежей с номерами страниц и кодами.
        """
        numbers_qr = []
        for page_num in range(len(self.qr_doc)):
            page = self.qr_doc[page_num]
            text = page.get_text()

            matches = re.findall(r'\b(\d{7})\s*\n\s*(\d{4})\b', text)

            if matches:
                code = ''.join(matches[0])
                numbers_qr.append((page_num, code))
                logger.info(f"Страница {page_num + 1}: Найден код {code}")
            else:
                logger.warning(f"Страница {page_num + 1}: Код не найден")

        return numbers_qr

    def extract_numbers_from_table(self) -> list[str]:
        """
        Извлекает числа из таблицы в PDF.

        :return: Список строк с найденными числами.
        """
        numbers_table = []
        with pdfplumber.open(io.BytesIO(self.pdf_table_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                table = page.extract_table()
                if table:
                    for row in table:
                        if row[-1].strip().isdigit():
                            number = row[-1].strip()
                            numbers_table.append(number)

        return numbers_table

    def create_sorted_pdf(self,
                          table_codes: list[str],
                          qr_codes: list[tuple[int, str]]) -> bytes:
        """
        Создает новый PDF с QR кодами на основе исходного PDF, сортируя страницы в соответствующем порядке.

        :param table_codes: Список кодов из таблицы.
        :param qr_codes: Список кортежей с номерами страниц и числовыми кодами
        :return: Отсортированный PDF в виде байтов.
        """
        output_doc = fitz.open()

        code_to_page = {code: page_num for page_num, code in qr_codes}

        for table_code in table_codes:
            if table_code in code_to_page:
                page_num = code_to_page[table_code]
                output_doc.insert_pdf(self.qr_doc, from_page=page_num, to_page=page_num)
                logger.info(f"Добавлена страница {page_num + 1} с кодом {table_code}")
            else:
                logger.warning(f"Предупреждение: код {table_code} не найден в PDF с QR кодами")

        output_pdf_bytes = io.BytesIO()
        output_doc.save(output_pdf_bytes,
                        garbage=4,
                        deflate=True,
                        clean=True,
                        linear=True)
        output_doc.close()

        return output_pdf_bytes.getvalue()