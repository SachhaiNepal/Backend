from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import (Multimedia, MultimediaAudio, MultimediaImage,
                               MultimediaVideo)

from multimedia.serializers.multimedia import MultimediaSerializer, MultimediaPOSTSerializer
from multimedia.serializers.multimedia_list import CreateMultimediaWithMultimediaListSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = Multimedia.objects.order_by("-uploaded_at")
    serializer_class = MultimediaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_approved"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return MultimediaPOSTSerializer
        return super(MultimediaViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        multimedia = self.get_object()
        multimedia_images = MultimediaImage.objects.filter(multimedia=multimedia)
        for image in multimedia_images:
            image.delete()
        multimedia_audios = MultimediaAudio.objects.filter(multimedia=multimedia)
        for audio in multimedia_audios:
            audio.delete()
        multimedia_videos = MultimediaVideo.objects.filter(multimedia=multimedia)
        for video in multimedia_videos:
            video.delete()
        multimedia.delete()
        return Response(
            {"message": "Multimedia deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CreateMultimediaWithMultimediaList(APIView):
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
        serializer = CreateMultimediaWithMultimediaListSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "True", "message": "Multimedia Created Successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleMultimediaApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
        except Multimedia.DoesNotExist:
            return Response(
                {"detail": "Multimedia does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        multimedia.is_approved = not multimedia.is_approved
        if multimedia.is_approved:
            multimedia.approved_by = request.user
            multimedia.approved_at = timezone.now()
        else:
            multimedia.approved_by = None
            multimedia.approved_at = None
        multimedia.save()
        return Response(
            {
                "success": True,
                "message": "Multimedia {} successfully.".format(
                    "approved" if multimedia.is_approved else "rejected"
                ),
            },
            status=status.HTTP_204_NO_CONTENT,
        )
