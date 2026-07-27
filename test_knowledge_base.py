from src.data_ingestion import create_knowledge_base


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


print("Knowledge Base Created Successfully!")