from src.pdf_loader import load_pdf
from src.website_ingestion import load_website_data
from src.text_splitter import split_documents

from src.embeddings import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    vector_store_exists,
)


def create_knowledge_base(pdf_paths, website_urls):

    # ==========================
    # Check if Vector DB Exists
    # ==========================

    if vector_store_exists():

        print("Loading existing Vector Database...")

        return load_vector_store()

    print("Creating new Knowledge Base...")

    all_documents = []

    # ==========================
    # Load PDF Documents
    # ==========================

    for pdf in pdf_paths:

        documents = load_pdf(pdf)

        all_documents.extend(documents)

    # ==========================
    # Load Website Documents
    # ==========================

    for url in website_urls:

        documents = load_website_data(url)

        all_documents.extend(documents)

    print(
        "Total Documents:",
        len(all_documents)
    )

    # ==========================
    # Split into Chunks
    # ==========================

    chunks = split_documents(
        all_documents
    )

    print(
        "Total Chunks:",
        len(chunks)
    )

    # ==========================
    # Create FAISS Vector Store
    # ==========================

    vector_store = create_vector_store(
        chunks
    )

    # ==========================
    # Save Vector Database
    # ==========================

    save_vector_store(
        vector_store
    )

    print("Knowledge Base Created Successfully!")

    return vector_store