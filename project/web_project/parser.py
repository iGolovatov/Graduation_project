import requests
from bs4 import BeautifulSoup
import time

HABR_SEARCH_URL = "https://habr.com/ru/search/"


def parse_habr_django_articles(page_limit=2):
    """
    Парсит статьи с Habr по запросу "django".
    """
    articles = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for page in range(1, page_limit + 1):
        params = {
            "q": "django",
            "target_type": "posts",
            "order": "relevance",
            "page": page
        }

        response = requests.get(HABR_SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        post_cards = soup.find_all("article", class_="tm-articles-list__item")

        for card in post_cards:
            title_tag = card.find("a", class_="tm-title__link")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = "https://habr.com" + title_tag["href"]
            author_tag = card.find("a", class_="tm-user-info__username")
            author = author_tag.text.strip() if author_tag else "Неизвестно"

            article_text = fetch_article_text(link, headers)

            articles.append({
                "title": title,
                "link": link,
                "author": author,
                "full_text": article_text[:10000],
                "summary": None
            })

        time.sleep(1)

    return articles


def fetch_article_text(article_url: str, headers: dict) -> str:
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find("div", id="post-content-body")
        if content:
            paragraphs = content.find_all(["p", "li"])
            text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            return text
        else:
            return "[Текст статьи не найден]"
    except Exception as e:
        return f"[Ошибка загрузки статьи: {str(e)}]"
