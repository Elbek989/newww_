import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError

from user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_customer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        user = User(**validated_data)

        # pattern = r'^(?=.*[A-Z])(?=.*\d).{4,}$'
        #
        # if not re.match(pattern, password):
        #     raise serializers.ValidationError(
        #         "Parol kamida 1 ta katta harf, 1 ta raqam bo‘lishi va uzunligi 4 tadan kam bo‘lmasligi kerak."
        #     )

        try:
            validate_password(password, user)
        except ValidationError as e:
            raise RestValidationError(e.messages)

        user.set_password(password)
        user.save()
        return user
