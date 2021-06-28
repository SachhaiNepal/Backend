from rest_framework import serializers

from utilities.models import (AboutUs, AboutUsImage, ContactUs, Feedback,
                              FeedbackFile, Service, ServiceImage,
                              ShowcaseGalleryImage, SliderImage)
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


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class ContactUsListSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()
    emails = serializers.SerializerMethodField()

    @staticmethod
    def get_contacts(obj):
        if obj.contacts:
            if "," in obj.contacts:
                return obj.contacts.split(",")
            else:
                return [obj.contacts]

    @staticmethod
    def get_emails(obj):
        if obj.emails:
            if "," in obj.emails:
                return obj.emails.split(",")
            else:
                return [obj.emails]

    class Meta:
        model = ContactUs
        fields = "__all__"


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
