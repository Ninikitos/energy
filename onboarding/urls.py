from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('step-one/', views.step_one, name='step-one'),
    path('step-two/<str:energy_choice>', views.step_two, name='step-two'),
    path('step-three/<str:energy_choice>/<str:emotion>', views.step_three, name='step-three')
]