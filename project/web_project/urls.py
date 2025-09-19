from django.urls import path
from . import views
from .views import HomeView, AboutView, BlogView, NewsCreateView, NewsDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('blog', BlogView.as_view(), name='blog'),
    path('blog/create', NewsCreateView.as_view(), name='create_news'),
    path('blog/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('api/edit-news/', views.NewsEditAjaxView.as_view(), name='api_edit_news'),
    path('api/edit-news/', views.NewsEditAjaxView.as_view(), name='api_edit_news'),
]
