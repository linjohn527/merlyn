# _*_ coding:utf-8 _*_
# __auth__: LJ

from rest_framework.generics import (
    ListAPIView
)

from  .serializers import (
    UserProfileSerializer
)

from ..customauth import (
    UserProfile
)


class UserProfileListAPIView(ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()