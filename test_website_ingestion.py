from src.website_ingestion import load_website_data


url = "https://www.atomcamp.com/"


documents = load_website_data(url)


print("\nTotal Website Documents:")
print(len(documents))


print("\nFirst Document:")
print(
    documents[0].page_content[:500]
)