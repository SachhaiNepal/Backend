from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Multimedia, PinMedia


class CreateOrTogglePinStatusOfMultimedia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            pin_media, created = PinMedia.objects.get_or_create(
                multimedia=multimedia, pinner=request.user
            )
            if created:
                pin_media.is_pinned = True
            else:
                pin_media.is_pinned = not pin_media.is_pinned
            pin_media.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Multimedia.DoesNotExist:
            return Response(
                {"detail": "Multimedia not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CreateOrTogglePinStatusOfArticle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            pin_media, created = PinMedia.objects.get_or_create(
                article=article, pinner=request.user
            )
            if created:
                pin_media.is_pinned = True
            else:
                pin_media.is_pinned = not pin_media.is_pinned
            pin_media.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Article.DoesNotExist:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )
