from src.pdf_loader import load_pdf


pdf_path = "data/sample.pdf"


documents = load_pdf(pdf_path)


print("Total Pages:", len(documents))


print("\nFirst Page Content:\n")

print(documents[0].page_content[:1000])