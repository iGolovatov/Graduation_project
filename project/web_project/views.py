from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView

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
