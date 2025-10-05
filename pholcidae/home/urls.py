from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('more_information/<id>', views.more_information, name='more_information'),
]
