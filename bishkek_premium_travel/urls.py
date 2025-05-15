# bishkek_premium_travel/urls.py
from django.contrib import admin
from django.urls import path, include # <-- Убедитесь, что include импортирован
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from hotels import views as hotel_views  # Импортируем views из hotels

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')), # <--- ДОБАВИТЬ ЭТОТ ПУТЬ ДЛЯ СМЕНЫ ЯЗЫКА
    path('', include('hotels.urls')), # URL вашего приложения hotels

    # URL для регистрации, входа, выхода
    path('accounts/signup/', hotel_views.signup_view, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'), # Выход остается POST

    # URL для личного кабинета
    path('account/', include('hotels.account_urls')),
]

# Раздача медиа файлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Раздача статики больше не нужна здесь, Django делает это сам при DEBUG=True