from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_vector_store


pdf_path = "data/sample.pdf"


documents = load_pdf(pdf_path)

chunks = split_documents(documents)


vector_store = create_vector_store(chunks)


print("Vector database created successfully!")