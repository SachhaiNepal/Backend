from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from multimedia import models
from multimedia.models import MultimediaAudio, MultimediaImage, MultimediaVideo
from multimedia.serializers.model_serializer import (
    ArticlePOSTSerializer,
    ArticleSerializer,
    MultimediaPOTSerializer,
    MultimediaSerializer,
)


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.order_by("-uploaded_at")
    serializer_class = MultimediaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_approved"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return MultimediaPOTSerializer
        return super(MultimediaViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        multimedia = self.get_object()
        multimedia_images = MultimediaImage.objects.filter(multimedia=multimedia)
        for image in multimedia_images:
            image.delete()
        multimedia_audios = MultimediaAudio.objects.filter(multimedia=multimedia)
        for audio in multimedia_audios:
            audio.delete()
        multimedia_videos = MultimediaVideo.objects.filter(multimedia=multimedia)
        for video in multimedia_videos:
            video.delete()
        multimedia.delete()
        return Response(
            {"message": "Multimedia deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.order_by("-uploaded_at")
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_approved"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return ArticlePOSTSerializer
        return super(ArticleViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = MultimediaImage.objects.filter(article=article)
        for image in article_images:
            image.delete()
        return Response(
            {"message": "Article deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
