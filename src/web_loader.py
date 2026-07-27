import requests
from bs4 import BeautifulSoup

from langchain_core.documents import Document


def load_website(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }


    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )


    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # Remove unnecessary parts
    for tag in soup(
        ["script", "style", "nav", "footer"]
    ):
        tag.decompose()


    text = soup.get_text(
        separator=" "
    )


    text = " ".join(
        text.split()
    )


    document = Document(
        page_content=text,
        metadata={
            "source": url
        }
    )


    return [document]