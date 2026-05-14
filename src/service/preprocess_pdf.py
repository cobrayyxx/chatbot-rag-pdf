from pypdf import PdfReader
import io

class PreprocessPDF:
    def __init__(self, pdf_contents):
        self.pdf_contents = pdf_contents

    def extract_pdf(self):
        pdf_stream = io.BytesIO(self.pdf_contents) # Convert bytes into a file-like stream object for PdfReader
        pdf_reader = PdfReader(pdf_stream)  # Create a PdfReader object from the file-like stream
        num_pages = len(pdf_reader.pages)        
        extracted_text = "" 

        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                extracted_text += f"\n\n--- Page {page_num + 1} ---\n\n{text}"

        return extracted_text, num_pages

        