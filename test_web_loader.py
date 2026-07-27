from src.web_loader import load_website


url = "https://atomcamp.com"


documents = load_website(url)


print("Documents:", len(documents))


print("\nWebsite Content:\n")

print(
    documents[0].page_content[:1000]
)