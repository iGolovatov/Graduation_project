from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404

from .forms import NewsForm
from .models import News


class HomeView(TemplateView):
    template_name = 'web_project/home.html'


class AboutView(TemplateView):
    template_name = 'web_project/about.html'


class BlogView(ListView):
    template_name = 'web_project/blog.html'
    model = News
    paginate_by = 3
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-created_at')


class NewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'web_project/create_news.html'
    form_class = NewsForm
    model = News
    success_url = reverse_lazy('blog')
    login_url = reverse_lazy('user_login')


class NewsDetailView(DetailView):
    template_name = 'web_project/news_detail.html'
    model = News
    context_object_name = 'news'


class NewsEditAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return JsonResponse({'error': 'Доступ запрещён'}, status=403)

        news_id = request.POST.get('news_id')
        if not news_id:
            return JsonResponse({'error': 'ID новости не указан'}, status=400)

        news = get_object_or_404(News, id=news_id)

        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title:
            return JsonResponse({'error': 'Заголовок обязателен'}, status=400)
        if not content:
            return JsonResponse({'error': 'Текст обязателен'}, status=400)

        news.title = title
        news.content = content

        if 'image' in request.FILES:
            news.image = request.FILES['image']

        try:
            news.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': f'Ошибка сохранения: {str(e)}'}, status=500)