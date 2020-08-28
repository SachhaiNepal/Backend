from rest_framework import serializers

from multimedia.models import Multimedia, MultimediaVideo, MultimediaAudio, Article, ArticleImage


class MultimediaVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaVideo
        fields = "__all__"


class MultimediaAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaAudio
        fields = "__all__"


class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        branch = Multimedia.objects.create(**validated_data)
        return branch

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = "__all__"


class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ["article"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        branch = Article.objects.create(**validated_data)
        return branch

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance
