from django.urls import path
from . import views

app_name = 'stages'

urlpatterns = [
    path('<int:case_id>/add/', views.add_stage, name='add_stage'),
    path('<int:case_id>/', views.view_stages, name='view_stages'),
]
