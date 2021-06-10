from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from article.serializers.action import CommentPostSerializer, CommentSerializer
from article.sub_models.action import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["article", "writer"]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CommentPostSerializer
        else:
            return CommentSerializer
