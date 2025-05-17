"""
URL configuration for lexdiary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import dashboard_view


from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'securepass123')
        return HttpResponse("Superuser created.")
    return HttpResponse("Superuser already exists.")


urlpatterns = [
    path('', dashboard_view, name='home'),  # 👈 This replaces previous login redirect
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls', namespace='users')),  # Register/login/logout
    path('cases/', include('cases.urls', namespace='cases')),
    path('hearings/', include('hearings.urls', namespace='hearings')),
    path('stages/', include('stages.urls', namespace='stages')),
    path('create-admin/', create_admin),




]