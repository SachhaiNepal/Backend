from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.user import (UserCreateSerializer,
                                       UserUpdateSerializer,
                                       UserWithProfileSerializer)
from accounts.sub_models.profile import CoverImage, ProfileImage


class ListUsersView(generics.ListAPIView):
    """
    Gets all the users in the database
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserWithProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]
    filterset_fields = ["is_staff"]


class ListFollower(APIView):
    """
    View to list all users in the system.
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        context = {"request": request}
        serializer = UserCreateSerializer(data=request.data, context=context)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                UserWithProfileSerializer(user, context=context).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def get(self, request, pk):
        """
        Returns single user by pk
        """
        context = {"request": request}
        user = self.get_object(pk)
        return Response(
            UserWithProfileSerializer(user, context=context).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """
        Updates user by pk
        """
        context = {"request": request}
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(
            user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserWithProfileSerializer(self.get_object(pk), context=context).data,
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies user by pk
        """
        context = {"request": request}
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserWithProfileSerializer(self.get_object(pk), context=context).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        profile = user.profile
        profile_images = ProfileImage.objects.filter(profile=profile)
        cover_images = CoverImage.objects.filter(profile=profile)
        [image.delete() for image in profile_images]
        [image.delete() for image in cover_images]
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
