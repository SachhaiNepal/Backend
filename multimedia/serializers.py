from django.db import IntegrityError
from rest_framework import serializers, status

from multimedia.models import Multimedia, MultimediaVideo, MultimediaAudio, Article, ArticleImage


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


class ArticleWithImageListSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False
        )
    )
    title = serializers.CharField(required=True, max_length=512)
    description = serializers.CharField(required=True, max_length=1024)

    def create(self, validated_data):
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")
        try:
            article, created = Article.objects.get_or_create(
                title=title,
                description=description,
                uploaded_by=user
            )
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "UNIQUE constraint failed: multimedia_media.title, multimedia_media.uploaded_by_id",
                "status": status.HTTP_400_BAD_REQUEST
            })

        if not created:
            raise serializers.ValidationError({"detail": "Article already exists.", "status": status.HTTP_400_BAD_REQUEST},)
        images = validated_data.pop('image')
        for image in images:
            ArticleImage.objects.create(
                image=image,
                article=article,
                **validated_data
            )
        return ArticleWithImageListSerializer(**validated_data)


class MultimediaWithMultimediaListSerializer(serializers.Serializer):
    video = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False
        )
    )
    audio = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False,
        )
    )
    title = serializers.CharField(required=True, max_length=512)
    description = serializers.CharField(required=True, max_length=1024)

    def create(self, validated_data):
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")
        try:
            multimedia, created = Multimedia.objects.get_or_create(
                title=title,
                description=description,
                uploaded_by=user
            )
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "UNIQUE constraint failed: multimedia_media.title, multimedia_media.uploaded_by_id",
                "status": status.HTTP_400_BAD_REQUEST
            })

        if not created:
            raise serializers.ValidationError({
                "detail": "Multimedia already exists.",
                "status": status.HTTP_400_BAD_REQUEST
            })

        videos = validated_data.pop('video')
        audios = validated_data.pop('audio')

        for video in videos:
            MultimediaVideo.objects.create(
                video=video,
                multimedia=multimedia,
                **validated_data
            )
        for audio in audios:
            MultimediaAudio.objects.create(
                audio=audio,
                multimedia=multimedia,
                **validated_data
            )
        return MultimediaWithMultimediaListSerializer(**validated_data)
