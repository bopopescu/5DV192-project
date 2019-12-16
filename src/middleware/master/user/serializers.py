from rest_framework import serializers

from user.models import User, UserSession


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'username coins date_registered'.split()


class UserSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSession
        fields = 'user session date_created'.split()
