from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.serializers.article import ArticleSerializer
from article.serializers.list import ArticleWithImageListSerializer
from article.sub_models.article import Article
from article.sub_models.media import ArticleImage


class ArticleWithImageListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request):
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
                ArticleImage.objects.create(image=image, article=article)
            article = ArticleSerializer(article, context={"request": request})
            return Response(article.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_approved", "created_by"]

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = ArticleImage.objects.filter(article=article)
        for image in article_images:
            image.delete()
        article.delete()
        return Response(
            {"message": "Article deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
