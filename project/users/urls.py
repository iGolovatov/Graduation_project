from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import SignUpView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]