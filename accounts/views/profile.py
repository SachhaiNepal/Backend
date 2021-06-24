from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, ProfileImage
from accounts.serializers.profile import (CoverImagePostSerializer,
                                          ProfileImageSerializer,
                                          ProfilePOSTSerializer,
                                          ProfileSerializer)
from accounts.serializers.user import UserWithProfileSerializer
from accounts.sub_models.profile import CoverImage


class UserProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        """
        Return a profile of a user
        """
        user = get_object_or_404(get_user_model(), pk=pk)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        """
        Returns particular profile
        """
        profile = self.get_object(pk)
        return Response(UserWithProfileSerializer(profile.user).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserWithProfileSerializer(profile.user).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserWithProfileSerializer(profile.user).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageViewSet(viewsets.ModelViewSet):
    queryset = ProfileImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer


class CoverImageViewSet(viewsets.ModelViewSet):
    queryset = CoverImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CoverImagePostSerializer


class SetActiveProfileImage(APIView):

    @staticmethod
    def get_object(pk):
        return get_object_or_404(ProfileImage, pk=pk)

    @staticmethod
    def unset_all_other_active(profile):
        profile_images = ProfileImage.objects.filter(profile=profile, active=True)
        if profile_images.count() > 0:
            for img in profile_images:
                img.active = False
                img.save()

    def put(self, request, pk):
        profile_image = self.get_object(pk)
        if not profile_image.active:
            self.unset_all_other_active(profile_image.profile)
            profile_image.active = True
            profile_image.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetActiveCoverImage(APIView):

    @staticmethod
    def get_object(pk):
        return get_object_or_404(CoverImage, pk=pk)

    @staticmethod
    def unset_all_other_active(profile):
        cover_images = CoverImage.objects.filter(profile=profile, active=True)
        if cover_images.count() > 0:
            for img in cover_images:
                img.active = False
                img.save()

    def put(self, request, pk):
        cover_image = self.get_object(pk)
        if not cover_image.active:
            self.unset_all_other_active(cover_image.profile)
            cover_image.active = True
            cover_image.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
