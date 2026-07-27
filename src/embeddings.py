import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Folder where FAISS database will be saved
VECTOR_DB_PATH = "vector_db"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store


def save_vector_store(vector_store):

    vector_store.save_local(
        VECTOR_DB_PATH
    )

    print("✅ Vector Database Saved!")


def load_vector_store():

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("✅ Vector Database Loaded!")

    return vector_store


def vector_store_exists():

    faiss_file = os.path.join(
        VECTOR_DB_PATH,
        "index.faiss"
    )

    pkl_file = os.path.join(
        VECTOR_DB_PATH,
        "index.pkl"
    )

    return (
        os.path.exists(faiss_file)
        and os.path.exists(pkl_file)
    )