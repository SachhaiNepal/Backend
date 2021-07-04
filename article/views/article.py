from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.serializers.article import CreateSerializer, ListSerializer
from article.serializers.list import ArticleWithImageListSerializer
from article.sub_models.article import Article
from article.sub_models.media import Image, CoverImage


# TODO: remove this endpoint
class ArticleWithImageListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @staticmethod
    def post(request):
        user = get_user_model().objects.get(username="admin")
        serializer = ArticleWithImageListSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            title = validated_data.get("title")
            description = validated_data.get("description")
            images = validated_data.get("image")
            article = Article.objects.create(
                title=title, created_by=user, description=description
            )
            for image in images:
                Image.objects.create(image=image, article=article)
            article = ListSerializer(article, context={"request": request})
            return Response(article.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_approved", "created_by", "completed_writing"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListSerializer
        return CreateSerializer

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = Image.objects.filter(article=article)
        article_cover = CoverImage.objects.filter(article=article)
        [image.delete() for image in article_images]
        [image.delete() for image in article_cover]
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StartWritingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        article, created = Article.objects.get_or_create(
            completed_writing=False, created_by=request.user
        )
        serializer = ListSerializer(article, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompleteWriting(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.created_by == request.user:
            article.completed_writing = True
            article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "Only writer is allowed to set completed state"},
            status=status.HTTP_403_FORBIDDEN,
        )
