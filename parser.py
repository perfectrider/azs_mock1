from bs4 import BeautifulSoup
import requests

url = 'https://habr.com/ru/articles/724242/'

urls = [
    'https://habr.com/ru/articles/724242/',
    'https://habr.com/ru/articles/783986/',
    'https://habr.com/ru/articles/786186/',
    'https://habr.com/ru/articles/783382/',
    'https://habr.com/ru/articles/page6/',
]

def url_to_text(url):
    url = url.split("://")[-1]
    url = url.replace("/", "_").replace(".", "_").replace("-", "_") + '.html'
    return url

for url in urls:
    page = requests.get(url)
    if page.status_code != 200:
        print(f'ERROR, url-{url} STATUS not OK!')
        continue

    soup = BeautifulSoup(page.text, "html.parser")
    name = url_to_text(url)

    with open(name, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
