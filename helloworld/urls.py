from django.urls import path

from .views import HelloWorldTemplateView

urlpatterns = [
    path('', HelloWorldTemplateView.as_view(), name='home')
    ]
