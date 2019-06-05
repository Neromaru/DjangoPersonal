from django.urls import path

from .views import (SignUpView,
                    ProfileView,
                    RrofileEditView,
                    PayCallbackView,
                    SubscriptionPaymentView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/profile/edit/', RrofileEditView.as_view(),
         name='profile_edit'),
    path('<int:pk>/subscription', SubscriptionPaymentView.as_view(),
         name='subscription'),
    path('<int:pk>/subscription/confirmation/', PayCallbackView.as_view())
    ]