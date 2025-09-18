from django.shortcuts import redirect
from django.views.generic import (
    CreateView, DetailView, UpdateView
)
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import (
    UserLoginForm, UserRegisterForm, UserProfileUpdateForm,
    UserPasswordChangeForm, CustomPasswordResetForm,
    CustomSetPasswordForm
)

User = get_user_model()


class UserRegisterView(CreateView):
    """Представление для регистрации нового пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """Запрещаем доступ аутентифицированным пользователям"""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Автоматический вход после регистрации"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация прошла успешно! Добро пожаловать!")
        return response


class UserLoginView(LoginView):
    """Представление для входа пользователя в систему"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Перенаправление после успешного входа"""
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('home')

    def form_valid(self, form):
        """Добавляем сообщение об успешном входе"""
        messages.success(self.request, "Вы успешно вошли в систему!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Добавляем сообщение об ошибке входа"""
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Представление для выхода пользователя из системы"""
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        """Добавляем сообщение после выхода"""
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Вы успешно вышли из системы!")
        return response


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра профиля пользователя"""
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        """Пользователь может смотреть только свой профиль"""
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя"""
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'

    def get_object(self, queryset=None):
        """Пользователь может редактировать только свой профиль"""
        return self.request.user

    def get_success_url(self):
        """Возвращаемся на страницу профиля с сообщением об успехе"""
        messages.success(self.request, "Профиль успешно обновлен!")
        return reverse_lazy('profile_detail')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Представление для смены пароля"""
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        """Добавляем сообщение об успешной смене пароля"""
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    """Представление для запроса восстановления пароля"""
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        """Добавляем сообщение об отправке email"""
        messages.success(self.request, "Инструкции по восстановлению пароля отправлены на ваш email.")
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Представление подтверждения отправки email"""
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Представление для установки нового пароля"""
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Представление подтверждения успешного сброса пароля"""
    template_name = 'users/password_reset_complete.html'
