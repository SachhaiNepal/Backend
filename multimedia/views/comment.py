from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, Comment, Multimedia
from multimedia.serializers.post_action import CommentSerializer, CommentPostSerializer


class ListArticleComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response({ "data": serializer.data }, status=status.HTTP_200_OK)


class ListMultimediaComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        multimedia = self.get_object(pk)
        comments = Comment.objects.filter(multimedia=multimedia)
        serializer = CommentSerializer(comments, many=True)
        return Response({ "data": serializer.data }, status=status.HTTP_200_OK)


class PostComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = CommentPostSerializer(
            data=request.data, context={ "request": request }
        )
        if serializer.is_valid():
            print(request.user)
            # serializer.writer = request.user
            print(serializer)
            serializer.save()
            return Response(
                { "success": True, "comment": serializer.data },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
