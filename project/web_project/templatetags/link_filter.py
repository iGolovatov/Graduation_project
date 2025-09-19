import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def make_links(text):
    # Regex для [текст](ссылка)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    replacement = r'<a href="\2">\1</a>'
    result = re.sub(pattern, replacement, text)
    return mark_safe(result)