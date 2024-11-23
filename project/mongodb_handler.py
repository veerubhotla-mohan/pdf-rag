from langchain_core.documents import Document
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import os

# method to store chunks  in the vector db using embedings 
def store_chunks_in_the_db(chunks, vector_store):
    # Create Documents to add to vector store
    documents = []
    for chunk in chunks:
        documents.append(Document(page_content=chunk))

    vector_store.add_documents(documents=documents)

def get_similar_documents(query, vector_store):
    docs = vector_store.similarity_search(query, k=4)
    return docs


def get_vector_store():
    try:
        uri = os.environ.get("MONGODB_URI")
        client = MongoClient(uri, server_api=ServerApi('1'))
        embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

        vector_store = MongoDBAtlasVectorSearch(
            collection=client["PDFDB"]["PDFCollection"],
            embedding=embeddings,
            index_name="vector_index_rag",
            relevance_score_fn="cosine",
        )
        return vector_store
    except Exception as e:
        print("Error in getting vector store", str(e))