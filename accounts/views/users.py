from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer


class ListUsers(APIView):
    """
    View to list all users in the system.
    * Only admin users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
