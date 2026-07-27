from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_vector_store
from src.chatbot import get_llm


pdf_path = "data/sample.pdf"


# Load PDF
documents = load_pdf(pdf_path)


# Split text
chunks = split_documents(documents)


# Create vector database
vector_store = create_vector_store(chunks)


# Get user question
question = "What is Machine Learning?"


# Search relevant chunks
docs = vector_store.similarity_search(question)


print("Relevant Information:\n")

print(docs[0].page_content)


# Ask Gemini
llm = get_llm()

response = llm.invoke(
    f"""
    Answer the question using this context:

    {docs[0].page_content}

    Question:
    {question}
    """
)


print("\nAI Answer:\n")

print(response.content)