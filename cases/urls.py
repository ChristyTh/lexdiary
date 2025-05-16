from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('add/', views.add_case, name='add_case'),
    path('', views.list_cases, name='list_cases'),
]
