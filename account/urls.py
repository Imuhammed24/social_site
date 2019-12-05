from django.urls import path
from .views import login_view, account_view, logout_view, register, edit, user_detail_view, user_list_view, user_follow
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name='login'),
    path('edit/', edit, name='edit'),
    path('profile/', account_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list_view, name='user-list'),
    path('follow/', user_follow, name='user-follow'),
    path('users/<username>/', user_detail_view, name='user-detail'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'), name='password_change'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html'), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('register/', register, name='register')


]
