from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.dashboard_list, name='dashboard_list'),
    path('dashboard/<slug:dashboard_slug>/', views.dashboard_detail, name='dashboard_detail'),
    path('api/<slug:dashboard_slug>/<slug:system_slug>/', views.add_deployment, name='add_deployment'),
]
