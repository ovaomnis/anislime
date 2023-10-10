from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import RegisterAPIView, ActivationAPIView, ChangePasswordAPIView, SendCodeAPIView, RecoveryPasswordAPIView, activate_view

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:code>/', activate_view, name='account_activate'),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('send-code/', SendCodeAPIView.as_view()),
    path('recovery-password/', RecoveryPasswordAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenObtainPairView.as_view()),
]
