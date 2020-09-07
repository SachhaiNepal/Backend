from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from multimedia import models
from multimedia import serializers


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.all()
    serializer_class = serializers.MultimediaSerializer
    # permission_classes = [permissions.IsAdminUser]


class MultimediaVideoViewSet(viewsets.ModelViewSet):
    queryset = models.MultimediaVideo.objects.all()
    serializer_class = serializers.MultimediaVideoSerializer
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class MultimediaAudioViewSet(viewsets.ModelViewSet):
    queryset = models.MultimediaAudio.objects.all()
    serializer_class = serializers.MultimediaAudioSerializer
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class MultimediaImageViewSet(viewsets.ModelViewSet):
    queryset = models.MultimediaImage.objects.all()
    serializer_class = serializers.MultimediaImageSerializer
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    # permission_classes = [permissions.IsAdminUser]


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = models.ArticleImage.objects.all()
    serializer_class = serializers.ArticleImageSerializer
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
