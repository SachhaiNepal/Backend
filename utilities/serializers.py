from rest_framework import serializers

from utilities.models import (
    AboutUs, AboutUsImage, Service, ShowcaseGalleryImage,
    SliderImage, ServiceImage, Feedback, FeedbackFile
)
from utils.global_serializer import UserWithActiveProfileMediaSerializer


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = "__all__"


class ShowcaseGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowcaseGalleryImage
        fields = "__all__"


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)


class ServiceListSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    writer = UserWithActiveProfileMediaSerializer()

    class Meta:
        model = Service
        fields = "__all__"


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = "__all__"


class AboutUsListSerializer(serializers.ModelSerializer):
    images = AboutUsImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUs
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)


class FeedbackFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackFile
        fields = "__all__"


class FeedbackReplySerializer(serializers.ModelSerializer):
    files = FeedbackFileSerializer(many=True, read_only=True)
    writer = UserWithActiveProfileMediaSerializer()

    class Meta:
        model = Feedback
        exclude = ["reply_to"]


class FeedbackListSerializer(serializers.ModelSerializer):
    files = FeedbackFileSerializer(many=True, read_only=True)
    writer = UserWithActiveProfileMediaSerializer()
    replies = FeedbackReplySerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)
