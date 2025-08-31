from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class HomePageView(RedirectView):
    template_name = 'home.html'

    def get_redirect_url(self):
        return reverse_lazy('home')
