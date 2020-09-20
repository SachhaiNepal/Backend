from rest_framework import permissions, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from advertise.models import Advertisement
from advertise.serializers import AdFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class AdFileViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdFileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    authentication_classes = (TokenAuthentication,)

    def destroy(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.image.delete()
        ad.delete()
        return Response({
            "message": "Advertisement deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
