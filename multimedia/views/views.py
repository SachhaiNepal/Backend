from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from multimedia import models
from multimedia.serializers.model_serializer import MultimediaSerializer, ArticleSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    # permission_classes = [permissions.IsAdminUser]


# class MultimediaVideoViewSet(viewsets.ModelViewSet):
#     queryset = models.MultimediaVideo.objects.all()
#     serializer_class = MultimediaVideoSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)
#
#
# class MultimediaAudioViewSet(viewsets.ModelViewSet):
#     queryset = models.MultimediaAudio.objects.all()
#     serializer_class = MultimediaAudioSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)
#
#
# class MultimediaImageViewSet(viewsets.ModelViewSet):
#     queryset = models.MultimediaImage.objects.all()
#     serializer_class = MultimediaImageSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [permissions.IsAdminUser]


# class ArticleImageViewSet(viewsets.ModelViewSet):
#     queryset = models.ArticleImage.objects.all()
#     serializer_class = ArticleImageSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)
