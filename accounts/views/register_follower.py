from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.user import RegisterFollowerSerializer
from location.models import Country, District, Province


class RegisterFollower(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def post(request):
        serializer = RegisterFollowerSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.data
            new_follower = get_user_model().objects.create(
                username=validated_data.get("username"),
                email=validated_data.get("email"),
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
            )
            new_follower.set_password(validated_data.pop("confirm_password"))
            new_follower.save()
            # update profile qualities
            new_follower.profile.contact = validated_data.get("contact")
            new_follower.profile.birth_date = validated_data.get("birth_date")
            new_follower.profile.current_city = validated_data.get("current_city")
            new_follower.profile.home_town = validated_data.get("home_town")
            new_follower.profile.country = Country.objects.get(
                id=validated_data.get("country")
            )
            new_follower.profile.province = Province.objects.get(
                id=validated_data.get("province")
            )
            new_follower.profile.district = District.objects.get(
                id=validated_data.get("district")
            )
            new_follower.profile.save()

            return Response(
                {
                    "message": "Follower registered successfully.",
                    "user": {
                        "username": new_follower.username,
                        "email": new_follower.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
