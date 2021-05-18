from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.serializers.article_list import *
from multimedia.serializers.article import ArticleSerializer, ArticlePOSTSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.order_by("-uploaded_at")
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_approved"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return ArticlePOSTSerializer
        return super(ArticleViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        article_images = ArticleImage.objects.filter(article=article)
        for image in article_images:
            image.delete()
        return Response(
            {"message": "Article deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CreateArticleWithImageList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @staticmethod
    def post(request):
        if request.user.is_anonymous:
            return Response(
                {
                    "details": "User must be logged in.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CreateArticleWithImageListSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "True", "message": "Article Created Successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleArticleApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.is_approved = not article.is_approved
            if article.is_approved:
                article.approved_by = request.user
                article.approved_at = timezone.now()
            else:
                article.approved_by = None
                article.approved_at = None
            article.save()
            return Response(
                {
                    "success": True,
                    "article": "Article {} successfully.".format(
                        "approved" if article.is_approved else "rejected"
                    ),
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Article.DoesNotExist:
            return Response(
                {"detail": "Article does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
