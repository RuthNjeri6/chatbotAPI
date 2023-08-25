from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import time
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')

DATA_PATH = "./api/first_80_papers"

# Supplying a persist_directory will store the embeddings on disk
persist_directory = './api/db'

# define what documents to load
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH, glob="./*.pdf", loader_cls=PyPDFLoader, show_progress=True, use_multithreading=True)
    documents = loader.load()

    #splitting the text into
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    ## here we are using OpenAI embeddings but in future we will swap out to local embeddings
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Embed and store the texts
    vectordb = Chroma.from_documents(documents=texts, 
                                    embedding=embedding,
                                    persist_directory=persist_directory)

    # persist the db to disk
    vectordb.persist()
    vectordb = None

if __name__ == "__main__":
    create_vector_db()
