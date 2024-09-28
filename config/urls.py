from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from item_app import views


urlpatterns = [
    # main ---------------------------------------------------------
    path('info/', views.info, name='info_url'),
    # other --------------------------------------------------------
    path('', views.root, name='root_url'),
    path('admin/', admin.site.urls),
    path('error_check/', views.error_check, name='error_check_url'),
    path('home/', views.home, name='home_url'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login_url'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout_url'),
    path('register/', views.register, name='register_url'),
    # path('items/<username>/', views.items, name='items_url'),
    path('version/', views.version, name='version_url'),
]
