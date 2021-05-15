from rest_framework import serializers

from utilities.models import (AboutUs, AboutUsImage, Service, ShowcaseGallery,
                              ShowcaseSlider)


class ShowcaseSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowcaseSlider
        fields = "__all__"


class ShowcaseGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowcaseGallery
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
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
    about_us_images = AboutUsImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUs
        fields = ["about_us", "created_at", "about_us_images"]
