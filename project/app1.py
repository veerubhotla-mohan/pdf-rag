from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.documents import Document
from langchain.chat_models.bedrock import BedrockChat
import os

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

def get_vector_store():
    try:
        uri = "mongodb+srv://veerubhotlashiva:RF7Ofb7dan9js26Y@cluster0.mtcyn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

        vector_store = MongoDBAtlasVectorSearch(
            collection=client["PDFDB"]["PDFCollection"],
            embedding=embeddings,
            index_name="vector_index_rag",
            relevance_score_fn="cosine"
        )
        return vector_store
    except Exception as e:
        print("Error in getting vector store", str(e))


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

def get_query_response(query, docs):
    context= "".join(doc.page_content + "\n" for doc in docs)
    bedrock_llm = BedrockChat(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")
    messages = [
        (
            "system",
            f"""You are a helpful assistant who can answers user's query with reference to some given context. The user's data is given below:
            <data>
            {context}
            </data>

            With reference to the above data, now answer the user's query. Be politeful and do not make any assumptions. Do not add any prefixes like "Based on the given data" or "Based on given context" or any similar prefixes. Start answering the user's query directly without any additional text or information. Do not mention anything about your source of data or the context.
            """,
        ),
        ("human", query),
    ]
    response = bedrock_llm.invoke(messages)
    return response.content


# def main():

#     query="what is cyber security"
#     vector_store =get_vector_store()
#     docs = get_similar_documents(query, vector_store)
#     get_query_response(query, docs)

# main()