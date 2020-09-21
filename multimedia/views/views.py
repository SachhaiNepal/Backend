from rest_framework import permissions, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from multimedia import models
from multimedia.models import MultimediaImage, MultimediaVideo, MultimediaAudio
from multimedia.serializers.model_serializer import MultimediaSerializer, ArticleSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
        return Response({
            "message": "Multimedia deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = MultimediaImage.objects.filter(article=article)
        for image in article_images:
            image.delete()
        return Response({
            "message": "Article deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
