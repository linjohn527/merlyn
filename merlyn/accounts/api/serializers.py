# _*_ coding:utf-8 _*_
# __auth__: LJ

from rest_framework.serializers import (
    ModelSerializer
)
from ..models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'name', 'is_admin']