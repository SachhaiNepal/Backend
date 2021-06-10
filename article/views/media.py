from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from article.serializers.article import ArticleImageSerializer
from article.sub_models.media import ArticleImage


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleImageSerializer

    def delete(self, request, pk):
        article_image = self.get_object(pk)
        article_image.image.delete()
        article_image.delete()
        return Response(
            {"success": True},
            status=status.HTTP_204_NO_CONTENT,
        )
