from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from core.telegram import send_telegram_message


@receiver(post_save, sender=News)
def order_services_changed(sender, instance, created, **kwargs):
    if created:
        created_at = instance.created_at.strftime("%d.%m.%Y %H:%M")

        message = (
            f"*🔔 У ВАС НА САЙТЕ ПРЕДЛОЖЕНИЕ НОВОСТИ! *\n\n"
            f"*Автор:* {instance.author}\n"
            f"*Заголовок:* `{instance.title}`\n"
            f"*Краткое содержание:* {instance.content[:255]}\n"
            f"*Дата создания:* {created_at}\n"
        )

        send_telegram_message(message)
