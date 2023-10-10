from rest_framework import serializers
from django.contrib.auth import get_user_model

from .tasks import send_activation_email, send_recovery_password_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('Passwords don\'t match')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = User.objects.create_user(**validated_data)
        host = request.build_absolute_uri('/')[:-1]
        send_activation_email.delay(email=user.email, code=user.code, host=host)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password2 = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong password!')
        return password

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password2')

        if p1 != p2:
            raise serializers.ValidationError('Passwords don\'t match')
        return attrs

    def set_new_password(self):
        request = self.context.get('request')
        user = request.user
        password = self._validated_data.get('new_password')
        user.set_password(password)
        user.save(update_fields=['password'])


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('The user with such mail was not found')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.generate_code()
        user.save()
        send_recovery_password_code.delay(user.email, user.code)


class RecoveryPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password2 = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        p1 = attrs.get('new_password')
        p2 = attrs.pop('new_password2')

        if not User.objects.filter(code=code, email=email).exists():
            raise serializers.ValidationError(
                'User with this email and code not found. Please double check is code or email are provided correctly')

        if p1 != p2:
            raise serializers.ValidationError('Passwords don\'t match')
        return attrs

    def set_new_password(self):
        code = self.validated_data.get('code')
        email = self.validated_data.get('email')
        password = self.validated_data.get('new_password')
        user = User.objects.get(email=email, code=code)
        user.set_password(password)
        user.code = ''
        user.save(update_fields=['password', 'code'])
