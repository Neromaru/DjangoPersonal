from django.urls import path

from .views import (SignUpView,
                    ProfileView,
                    RrofileEditView,
                    PayCallbackView,
                    SubscriptionPaymentView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', RrofileEditView.as_view(),
         name='profile_edit'),
    path('subscription', SubscriptionPaymentView.as_view(),
         name='subscription'),
    path('subscription/confirmation/', PayCallbackView.as_view())
    ]