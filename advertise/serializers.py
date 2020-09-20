from rest_framework import serializers

from advertise.models import Advertisement


class AdFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = "__all__"

    # def create(self, validated_data):
    #     validated_data["created_by"] = self.context["request"].user
    #     ad_file = AdFile.objects.create(**validated_data)
    #     return ad_file

    # def update(self, instance, validated_data):
    #     instance.updated_by = self.context["request"].user
    #     instance.save()
    #     return instance

    # def delete(self, instance, validated_data):
    #     instance.image.delete()
    #     return instance
