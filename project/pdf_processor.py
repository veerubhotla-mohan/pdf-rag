from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

# method to create chunks from pdf
def create_chunks_from_pdf(pdf_text):
    try:
        # pdf_reader=PdfReader(pdf_path)
        # text =""
        # for page in pdf_reader.pages:
        #     text+=page.extract_text()
        text_splitter=CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200)

        chunks=text_splitter.split_text(pdf_text)
        return chunks

    except Exception as e:
        print(f"Error processing documents: {e}")
        return ""


# method to store chunks  in the vector db using embedings
def store_chunks_in_the_db(chunks, vector_store):
    # Create Documents to add to vector store
    documents = []
    for chunk in chunks:
        documents.append(Document(page_content=chunk))

    vector_store.add_documents(documents=documents)
    print("Chunks stored in vector DB")