from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from event.models import Event, EventPhoto, EventVideoUrls
from utils.file import check_size


class EventSerializer(serializers.ModelSerializer):
    contact = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Event
        fields = "__all__"

    def validate_banner(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        try:
            k = data['municipality']
            try:
                k = data['vdc']
                raise serializers.ValidationError("Both municipality and vdc cannot be assigned.")
            except KeyError:
                return data
        except KeyError:
            try:
                k = data['vdc']
                return data
            except KeyError:
                raise serializers.ValidationError("One of the municipality or vdc must be assigned.")

    def create(self, validated_data):
        # validated_data["created_by"] = self.context["request"].user
        if validated_data["is_approved"]:
            # validated_data["approved_by"] = self.context["request"].user
            validated_data["approved_at"] = timezone.now()
        print(validated_data)
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        if not instance.is_approved and validated_data.is_approved:
            validated_data["approved_by"] = self.context["request"].user
            validated_data["approved_at"] = timezone.now()
        if not validated_data.is_approved and instance.is_approved:
            validated_data["approved_by"] = None
            validated_data["approved_at"] = None
        return super().update(instance, validated_data)


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj


class EventVideoUrlsSerializer(serializers.ModelSerializer):
    video_urls = serializers.ListField(child=serializers.URLField(validators=[
        RegexValidator(
            regex=r"https:\/\/www\.youtube\.com\/*",
            message="URL must be sourced from youtube."
        )
    ]))

    class Meta:
        model = EventVideoUrls
        fields = "__all__"
