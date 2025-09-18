from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(_('Заголовок новости'), max_length=200)
    content = models.TextField(_('Содержание новости'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    author = models.CharField(_('Автор'), max_length=100)
    is_published = models.BooleanField(_('Опубликовано'), default=False)
    image = models.ImageField(_('Изображение'), upload_to='news_images/', blank=True, null=True)

    class Meta:
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
