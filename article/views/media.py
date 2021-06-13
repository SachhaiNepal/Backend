from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from article.serializers.article import (CoverImageCreateSerializer,
                                         CoverImageSerializer, ImageSerializer,
                                         ImageUrlCreateSerializer,
                                         ImageUrlSerializer)
from article.sub_models.media import CoverImage, Image, ImageUrl


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def delete(self, request, pk):
        article_image = self.get_object(pk)
        article_image.image.delete()
        article_image.delete()
        return Response(
            {"success": True},
            status=status.HTTP_204_NO_CONTENT,
        )


class CoverImageViewSet(viewsets.ModelViewSet):
    queryset = CoverImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CoverImageSerializer
        return CoverImageCreateSerializer

    def delete(self, request, pk):
        article_cover_image = self.get_object(pk)
        article_cover_image.image.delete()
        article_cover_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleImageUrlViewSet(viewsets.ModelViewSet):
    queryset = ImageUrl.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "delete"]:
            return ImageUrlSerializer
        return ImageUrlCreateSerializer
