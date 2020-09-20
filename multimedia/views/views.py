from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from multimedia import models
from multimedia.models import MultimediaImage, MultimediaVideo, MultimediaAudio
from multimedia.serializers.model_serializer import MultimediaSerializer, ArticleSerializer
from multimedia.models import Multimedia, Article


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    # permission_classes = [permissions.IsAdminUser]

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
    # permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = MultimediaImage.objects.filter(article=article)
        for image in article_images:
            image.delete()
        return Response({
            "message": "Article deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ToggleArticleView(APIView):
    authentication_classes = [TokenAuthentication]
     
    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({
                "detail": "Member does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        article.is_approved = not article.is_approved
        # article.approved_by = Article.objects.get(user=request.user)
        article.save()
        return Response({
            "article": "Artticle {} successfully.".format("approved" if article.is_approved else "rejected")
        }, status=status.HTTP_204_NO_CONTENT)

    
    

class ToggleMultimediaApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
     
    def post(self, request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
        except Multimedia.DoesNotExist:
            return Response({
                "detail": "Member does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        multimedia.is_approved = not multimedia.is_approved
        # multimedia.approved_by = Multimedia.objects.get(user=request.user)
        multimedia.save()
        return Response({
            "message": "Multimedia {} successfully.".format("approved" if multimedia.is_approved else "rejected")
        }, status=status.HTTP_204_NO_CONTENT)
