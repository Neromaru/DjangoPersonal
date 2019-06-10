from django.urls import path, include
from .views import IndexView, NotificationView, NotifcationListView, \
    DeleteNotificationView, EditNotificationView

notification_pattern = [
    path('user_<int:pk>/add', NotificationView.as_view(),
         name='notify'),
    path('user_<int:pk>/', NotifcationListView.as_view(),
         name='notification_list'),
    path('user_<int:pk>/edit/<int:pk1>', EditNotificationView.as_view(),
         name='edit_notification'),
    path('user_<int:pk>/delete/<int:pk1>', DeleteNotificationView.as_view(),
         name='delete_notification')

    ]

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('notifications/', include(notification_pattern))
    ]
