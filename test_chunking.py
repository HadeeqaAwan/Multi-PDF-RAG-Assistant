from src.pdf_loader import load_pdf
from src.text_splitter import split_documents


pdf_path = "data/sample.pdf"


documents = load_pdf(pdf_path)


chunks = split_documents(documents)


print("Total Documents:", len(documents))

print("Total Chunks:", len(chunks))


print("\nFirst Chunk:\n")

print(chunks[0].page_content)