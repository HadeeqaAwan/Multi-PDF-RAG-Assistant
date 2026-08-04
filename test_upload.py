import requests

url = "http://127.0.0.1:8000/upload"

with open("data/Introduction to Natural Language Processing (NLP).pdf", "rb") as f:
    files = [
        ("files", ("sample.pdf", f, "application/pdf"))
    ]

    response = requests.post(url, files=files)

print(response.status_code)
print(response.text)