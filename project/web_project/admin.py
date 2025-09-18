from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_filter = ('is_published',)
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        updated_count = queryset.update(is_published=True)
        self.message_user(request, f'{updated_count} новостей были опубликованы.')

    make_published.short_description = 'Опубликовать выбранные новости'

    def make_unpublished(self, request, queryset):
        updated_count = queryset.update(is_published=False)
        self.message_user(request, f'{updated_count} новостей были сняты с публикации.')

    make_unpublished.short_description = 'Снять с публикации выбранные новости'
