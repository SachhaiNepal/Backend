from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Love, Article, Multimedia
from multimedia.serializers.post_action import LoveSerializer


# TODO: set url
class LovedArticlesList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        context = { "request": request }
        loved_articles = Love.objects.filter(multimedia=None)
        serializer = LoveSerializer(data=loved_articles, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO: set url
class LovedMultimediaList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        context = { "request": request }
        loved_multimedias = Love.objects.filter(article=None)
        serializer = LoveSerializer(data=loved_multimedias, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrToggleLoveStatusOfArticle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            love, created = Love.objects.get_or_create(
                article=article, lover=request.user
            )
            if created:
                love.is_loved = True
            else:
                love.is_loved = not love.is_loved
            love.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Article.DoesNotExist:
            return Response(
                { "detail": "Article not found." }, status=status.HTTP_404_NOT_FOUND
            )


class CreateOrToggleLoveStatusOfMultimedia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            love, created = Love.objects.get_or_create(
                multimedia=multimedia, lover=request.user
            )
            if created:
                love.is_loved = True
            else:
                love.is_loved = not love.is_loved
            love.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Multimedia.DoesNotExist:
            return Response(
                { "detail": "Multimedia not found." }, status=status.HTTP_404_NOT_FOUND
            )
