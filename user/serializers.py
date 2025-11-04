import re

from rest_framework import serializers

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


        pattern = r'^(?=.*[A-Z])(?=.*\d).{4,}$'

        if not re.match(pattern, password):
            raise serializers.ValidationError(
                "Parol kamida 1 ta katta harf, 1 ta raqam bo‘lishi va uzunligi 4 tadan kam bo‘lmasligi kerak."
            )

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
