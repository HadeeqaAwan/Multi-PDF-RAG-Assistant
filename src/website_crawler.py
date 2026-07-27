import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def get_public_links(base_url, limit=5):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "Chrome/120 Safari/537.36"
        )
    }


    response = requests.get(
        base_url,
        headers=headers,
        timeout=15
    )


    response.raise_for_status()


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    links = []


    for tag in soup.find_all("a"):

        href = tag.get("href")


        if href:

            url = urljoin(
                base_url,
                href
            )


            domain = urlparse(url).netloc
            base_domain = urlparse(base_url).netloc


            # Keep only same website public pages
            if (
                domain == base_domain
                and url not in links
                and "#" not in url
            ):
                links.append(url)


    return links[:limit]