from src.source_formatter import format_sources
from src.data_ingestion import create_knowledge_base
from src.chatbot import get_llm


pdfs = [
    "data/sample.pdf"
]


websites = [
    "https://www.atomcamp.com/"
]


vector_store = create_knowledge_base(
    pdfs,
    websites
)


question = "What is Machine Learning?"


docs = vector_store.similarity_search(
    question,
    k=3
)


context = "\n\n".join(
    [doc.page_content for doc in docs]
)


llm = get_llm()


response = llm.invoke(
    f"""
    Answer the question using only the context.

    Context:
    {context}

    Question:
    {question}
    """
)


print("\nAnswer:")
print(response.content)


print("\nSources:")

sources = format_sources(docs)

print("\nSources:")

for source in sources:
    print(source)