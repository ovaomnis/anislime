from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from apps.account.serializers import *


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            'You have successfully registered. An activation email has been sent to you',
            status=201
        )


class ActivationAPIView(APIView):

    def get(self, request, code):
        user = get_object_or_404(User, code=code)
        user.is_active = True
        user.code = ''
        user.save(update_fields=['is_active', 'code'])
        return Response('Success', status=200)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Password has been successfully updated', status=200)


class SendCodeAPIView(APIView):
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('An email with code has been sent to this email', status=200)


class RecoveryPasswordAPIView(APIView):
    def post(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been successfully updated', status=200)
