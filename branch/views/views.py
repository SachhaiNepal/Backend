from rest_framework import viewsets, status
from rest_framework.response import Response

from branch.serializers import *


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BranchPostSerializer
        return super(BranchViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        branch = self.get_object()
        branch.image.delete()
        branch.delete()
        return Response({
            "message": "Event deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
