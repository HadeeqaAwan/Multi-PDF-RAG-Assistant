from src.website_crawler import get_public_links


url = "https://www.atomcamp.com/"


pages = get_public_links(url)


print("Pages Found:")

for page in pages:
    print(page)