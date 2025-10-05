from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('more_information/<id>', views.more_information, name='more_information'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
]
