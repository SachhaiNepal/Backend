from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from advertise.models import Advertisement
from advertise.serializers import AdFileSerializer


class AdFileViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdFileSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.image.delete()
        ad.delete()
        return Response(
            {"message": "Advertisement deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
