from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path("", views.index, name="index"),  
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("destination/", views.destination, name="destination"),
    path("blog/", views.blog, name="blog"),
    path("articles/", views.article_list, name="article_list"),  # 👈 correspond au {% url 'article_list' %}
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),

        path('logout/', views.logout_view, name='logout'),

    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),


     path('destination/<int:destination_id>/reservation/', views.reservation, name='reservation'),
    path('process-reservation/', views.process_reservation, name='process_reservation'),
    path('reservation-confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    
    
    # Réinitialisation mot de passe
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        form_class=CustomPasswordResetForm,
        success_url='/password-reset/done/'
    ), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            form_class=CustomSetPasswordForm,
            success_url='/password-reset/complete/'
        ), name='password_reset_confirm'),
    
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    
]