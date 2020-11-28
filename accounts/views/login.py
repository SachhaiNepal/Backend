from django.contrib.auth import authenticate, get_user_model, logout
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import (LoginSerializer, LogoutSerializer,
                                  UserCreateSerializer)


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
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "data" : serializer.data
                }, status=status.HTTP_202_ACCEPTED)
            return Response(
                {"detail": "Login Failed! Provide Valid Authentication Credentials."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
                if not user.is_authenticated:
                    return Response({
                        "detail": "User not logged in."
                    }, status=status.HTTP_400_BAD_REQUEST)
                logout(request)
                try:
                    token = Token.objects.get(user=user)
                    token.delete()
                    return Response({
                        "detail": "User member '{}' logged out successfully.".format(user.username)
                    }, status=status.HTTP_204_NO_CONTENT)
                except Token.DoesNotExist:
                    return Response({
                        "detail": "User '{}' logged out successfully.".format(user.username)
                    }, status=status.HTTP_204_NO_CONTENT)
            except get_user_model().DoesNotExist:
                return Response({
                    "detail": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
