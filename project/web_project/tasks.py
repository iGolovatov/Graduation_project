from .parser import parse_habr_django_articles
from .summarize import summarize_text
from celery import shared_task
from logging import getLogger
from .models import News

logger = getLogger(__name__)


@shared_task
def parse_news():
    try:
        logger.info("Начинаем парсинг статей с Habr по теме Django...")
        articles = parse_habr_django_articles(page_limit=1)

        logger.info(f"Найдено {len(articles)} статей. Генерируем пересказы...")

        news = []
        for i, article in enumerate(articles):
            logger.info(f"Обработка статьи {i + 1}/{len(articles)}: {article['title'][:50]}...")
            summary = summarize_text(article["full_text"])
            article["summary"] = summary
            news.append(News(
                title=article["title"],
                author=article["author"],
                content=article["summary"] + f"\n\n[полная версия]({article['link']})",
                is_published=True,
            ))

        News.objects.bulk_create(news)
        logger.info(f"Сохранено {len(news)} новостей в базу данных.")

        logger.info("✅ Парсинг и суммаризация завершены.")

    except Exception as exc:
        logger.error(f"❌ Ошибка в задаче: {exc}")
