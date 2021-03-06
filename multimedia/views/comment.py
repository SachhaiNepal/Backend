from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from multimedia.models import Comment
from multimedia.serializers.action import (CommentPostSerializer,
                                           CommentSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["multimedia", "writer"]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CommentPostSerializer
        else:
            return CommentSerializer
