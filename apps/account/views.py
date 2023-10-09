from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.account.serializers import (RegisterSerializer,
                                      ChangePasswordSerializer,
                                      SendCodeSerializer,
                                      RecoveryPasswordSerializer)

User = get_user_model()


class RegisterAPIView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
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

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Password has been successfully updated', status=200)


class SendCodeAPIView(APIView):
    @swagger_auto_schema(request_body=SendCodeSerializer)
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('An email with code has been sent to this email', status=200)


class RecoveryPasswordAPIView(APIView):
    @swagger_auto_schema(request_body=RecoveryPasswordSerializer)
    def post(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been successfully updated', status=200)
