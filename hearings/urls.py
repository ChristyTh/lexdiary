from django.urls import path
from . import views

app_name = 'hearings'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('<int:case_id>/add/', views.add_hearing, name='add_hearing'),
    path('<int:case_id>/', views.view_hearings, name='view_hearings'),
]
