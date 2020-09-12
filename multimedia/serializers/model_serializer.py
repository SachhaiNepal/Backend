from rest_framework import serializers

from multimedia.models import MultimediaVideo, MultimediaAudio, MultimediaImage, Multimedia, ArticleImage, Article


class MultimediaVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaVideo
        fields = "__all__"
        depth = 1


class MultimediaAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaAudio
        fields = "__all__"
        depth = 1


class MultimediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaImage
        fields = "__all__"
        depth = 1


class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
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
        depth = 1


class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ["article"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        branch = Article.objects.create(**validated_data)
        return branch

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance
