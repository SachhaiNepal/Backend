from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event, EventPhoto, EventVideoUrls
from event.serializers import EventPhotoSerializer, EventVideoUrlsSerializer
from utils.helper import generate_url_for_media_resources


class ListEventPhotos(APIView):
    @staticmethod
    def get(request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event_photos = EventPhoto.objects.filter(event=event)
            serializer = EventPhotoSerializer(event_photos, many=True)
            serializer = generate_url_for_media_resources(serializer, "image")
            return Response({
                "count": event_photos.count(),
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({
                "details": "Event not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListEventVideoUrls(APIView):
    @staticmethod
    def get(request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event_video_urls = EventVideoUrls.objects.filter(event=event)
            serializer = EventVideoUrlsSerializer(event_video_urls, many=True)
            return Response({
                "count": event_video_urls.count(),
                "data" : serializer.data
            }, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({
                "details": "Event not found."
            }, status=status.HTTP_404_NOT_FOUND)
