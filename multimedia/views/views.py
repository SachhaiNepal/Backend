from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from multimedia import models
from multimedia.serializers.model_serializer import MultimediaSerializer, ArticleSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = models.Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    # permission_classes = [permissions.IsAdminUser]

    # def destroy(self, request, *args, **kwargs):
    #     multimedia = self.get_object()
    #     return Response({
    #         "message": "Multimedia deleted successfully."
    #     }, status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [permissions.IsAdminUser]

    # def destroy(self, request, *args, **kwargs):
    #     article = self.get_object()
    #     return Response({
    #         "message": "Article deleted successfully."
    #     }, status=status.HTTP_204_NO_CONTENT)
