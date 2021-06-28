from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
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
    filterset_fields = ["article"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        article_image = self.get_object()
        article_image.image.delete()
        article_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoverImageViewSet(viewsets.ModelViewSet):
    queryset = CoverImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["article"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
    filterset_fields = ["article"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "delete"]:
            return ImageUrlSerializer
        return ImageUrlCreateSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
