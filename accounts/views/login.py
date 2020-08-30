from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers import UserCreateSerializer, LoginSerializer, LogoutSerializer


class LoginView(APIView):
    @staticmethod
    def post(request):
        """
        Login a user instance
        Provides a brand new token for a member user
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            try:
                get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return Response({"detail": "User '" + username + "' Not Found!"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(username=username, password=password)
            if user:
                user.last_login = timezone.now()
                if not user.is_active:
                    user.is_active = True
                    user.save()
                serializer = UserCreateSerializer(user)
                try:
                    Member.objects.get(user=user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "token": token.key,
                        "data": serializer.data
                    }, status=status.HTTP_202_ACCEPTED)
                except Member.DoesNotExist:
                    return Response({
                        "data": serializer.data
                    }, status=status.HTTP_202_ACCEPTED)
            return Response(
                {"detail": "Login Failed! Provide Valid Authentication Credentials."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @staticmethod
    def post(request):
        """
        Logs out a user instance
        Removes member user token from database
        """
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            try:
                user = get_user_model().objects.get(username=username)
                try:
                    token = Token.objects.get(user=user)
                    token.delete()
                    return Response({
                        "message": "User Member '{}' Logged Out Successfully.".format(user.username)
                    }, status=status.HTTP_204_NO_CONTENT)
                except Token.DoesNotExist:
                    return Response({
                        "message": "User '{}' Logged Out Successfully.".format(user.username)
                    }, status=status.HTTP_204_NO_CONTENT)
            except get_user_model().DoesNotExist:
                return Response({
                    "detail": "Logout Failed! User Not Found."
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
