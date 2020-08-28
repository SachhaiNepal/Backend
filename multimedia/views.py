from rest_framework import permissions, viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Multimedia, MultimediaVideo, MultimediaAudio, Article, ArticleImage
from multimedia.serializers import MultimediaSerializer, MultimediaVideoSerializer, \
    MultimediaAudioSerializer, ArticleSerializer, ArticleImageSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [permissions.IsAdminUser]


class MultimediaVideoViewSet(viewsets.ModelViewSet):
    queryset = MultimediaVideo.objects.all()
    serializer_class = MultimediaVideoSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class MultimediaAudioViewSet(viewsets.ModelViewSet):
    queryset = MultimediaAudio.objects.all()
    serializer_class = MultimediaAudioSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAdminUser]


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

