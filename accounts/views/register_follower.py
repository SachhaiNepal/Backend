from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.user import RegisterFollowerSerializer
from location.models import Country, Province, District


class RegisterFollower(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def post(request, get_user_model=None):
        serializer = RegisterFollowerSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.data
            new_follower = get_user_model().objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
            )
            new_follower.set_password(validated_data.pop("confirm_password"))
            new_follower.save()
            # update profile qualities
            new_follower.profile.contact = validated_data["contact"]
            new_follower.profile.birth_date = validated_data["birth_date"]
            new_follower.profile.current_city = validated_data["current_city"]
            new_follower.profile.home_town = validated_data["home_town"]
            new_follower.profile.country = Country.objects.get(
                id=validated_data["country"]
            )
            new_follower.profile.province = Province.objects.get(
                id=validated_data["province"]
            )
            new_follower.profile.district = District.objects.get(
                id=validated_data["district"]
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
