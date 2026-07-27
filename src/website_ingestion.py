from src.website_crawler import get_public_links
from src.web_loader import load_website


def load_website_data(base_url):

    pages = get_public_links(
        base_url,
        limit=10
    )


    all_documents = []


    for page in pages:

        try:
            documents = load_website(page)

            all_documents.extend(documents)

            print(
                "Loaded:",
                page
            )

        except Exception as e:

            print(
                "Failed:",
                page,
                e
            )


    return all_documents