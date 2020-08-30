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
        article, created = Article.objects.get_or_create(
            title=title,
            description=description,
            uploaded_by=user
        )
        if not created:
            raise serializers.ValidationError("Blog already exists.")
        images = validated_data.pop('image')
        for image in images:
            ArticleImage.objects.create(
                image=image,
                article=article,
                **validated_data
            )
        return ArticleWithImageListSerializer(**validated_data)
