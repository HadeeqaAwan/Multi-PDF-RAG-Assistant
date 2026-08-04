from src.embeddings import load_vector_store
from src.chatbot import get_llm


def ask_question(question):

    vector_store = load_vector_store()

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    llm = get_llm()

    response = llm.invoke(
        f"""
You are an AI Assistant.

Answer ONLY using the given context.

Context:
{context}

Question:
{question}
"""
    )

    sources = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            0
        )

        sources.append(
            {
                "file": source,
                "page": page + 1
            }
        )

    return {
        "answer": response.content,
        "sources": sources
    }