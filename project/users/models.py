from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    middle_name = models.CharField(_('Отчество'), blank=True, null=True)
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', blank=True, null=True)
    telegram_id = models.CharField(_('Telegram ID'), max_length=100, blank=True, null=True)
    github_id = models.CharField(_('GitHub ID'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
