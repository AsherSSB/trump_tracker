import requests
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self):
        self.urls = [
            "https://www.bbc.com", 
            "https://www.cnn.com",
            "https://www.foxnews.com/",
            "https://www.newsmax.com/",
            "https://www.nbcnews.com/",
            "https://www.wsj.com/",
        ]

    def get_headlines(self):
        headlines = []
        for url in self.urls:
            retrieved_headlines = self.send_request(url)
            headlines += retrieved_headlines     
        return headlines

    def send_request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            headlines = []
            links = []

            for tag in soup.find_all(['h1', 'h2', 'h3']):
                link = tag.find('a')
                text = tag.get_text(strip=True) 
                if link and "Trump" in text and text not in headlines:
                    headlines.append(text)
                    href = link.get('href', '')
                    if href.startswith('/'):
                        href = f"{url.rstrip('/')}{href}"
                    links.append(href)

            for link in soup.find_all('a'):
                heading = link.find(['h1', 'h2', 'h3'])
                if heading and "Trump" in heading.get_text() and heading.get_text(strip=True) not in headlines:
                    headlines.append(heading.get_text(strip=True))
                    href = link.get('href', '')
                    if href.startswith('/'):
                        href = f"{url.rstrip('/')}{href}"
                    links.append(href)

            return list(zip(headlines, links))
        return []
