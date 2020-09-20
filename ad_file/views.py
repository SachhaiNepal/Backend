from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication



from ad_file.models import AdFile
from ad_file.serializers import AdFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser




class AdFileViewSet(viewsets.ModelViewSet):
    queryset = AdFile.objects.all()
    serializer_class = AdFileSerializer
    parser_classes = (MultiPartParser, FormParser,)



class ToggleAdFileView(APIView):
    
    authentication_classes = [TokenAuthentication]
     
    def post(self, request, pk):
        try:
            AdFile = AdFile.objects.get(pk=pk)
        except AdFile.DoesNotExist:
            return Response({
                "detail": "advertisement does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        AdFile.is_approved = not AdFile.is_approved
        # article.approved_by = Article.objects.get(user=request.user)
        AdFile.save()
        return Response({
            "AdFile": "Advertisement {} successfully.".format("approved" if AdFile.is_approved else "rejected")
        }, status=status.HTTP_204_NO_CONTENT)

    


