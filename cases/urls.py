from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.list_cases, name='list_cases'),
    path('add/', views.add_case, name='add_case'),
    path('<int:pk>/edit/', views.edit_case, name='edit_case'),
    path('<int:pk>/delete/', views.delete_case, name='delete_case'),
]
