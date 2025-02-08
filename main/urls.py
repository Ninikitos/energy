from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('emotions', views.emotions, name='emotions'),
    path('emotions/all', views.emotions_all, name='emotions-all'),
]