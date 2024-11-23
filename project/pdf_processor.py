from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

# method to create chunks from pdf
def create_chunks_from_pdf(pdf_path):
    try:
        pdf_reader=PdfReader(pdf_path)
        text =""
        for page in pdf_reader.pages:
            text+=page.extract_text()
        text_splitter=CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200) 
                                         
        chunks=text_splitter.split_text(text)
        return chunks

    except Exception as e:
        print(f"Error processing documents: {e}")
        return ""