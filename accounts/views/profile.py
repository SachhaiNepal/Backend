from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, ProfileImage
from accounts.serializers.profile import ProfileSerializer, ProfilePOSTSerializer, ProfileImagePostSerializer


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
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully.",
                    "data": ProfileSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
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
                {
                    "message": "Profile patched successfully.",
                    "data": ProfileSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageViewSet(viewsets.ModelViewSet):
    queryset = ProfileImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImagePostSerializer
