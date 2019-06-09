from django.urls import path
from .views import IndexView, NotificationView


urlpatterns = [
    path('', IndexView.as_view(), name="main"),
    path('notifications/user_<int:pk>/add', NotificationView.as_view(),
         name='notify')
    ]
