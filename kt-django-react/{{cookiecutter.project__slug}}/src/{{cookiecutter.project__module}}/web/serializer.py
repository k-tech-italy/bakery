from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Invalid credentials')
            return user
        raise ValidationError('Must include "username" and "password"')
