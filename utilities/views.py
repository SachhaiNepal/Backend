from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.settings import MAX_SHOWCASE_GALLERY_IMAGES
from utilities.models import (AboutUs, AboutUsImage, ContactUs, Feedback,
                              FeedbackFile, Service, ServiceImage,
                              ShowcaseGalleryImage, SliderImage)
from utilities.serializers import (AboutUsImageSerializer,
                                   AboutUsListSerializer, AboutUsSerializer,
                                   ContactUsListSerializer,
                                   ContactUsSerializer, FeedbackListSerializer,
                                   FeedbackSerializer, ServiceImageSerializer,
                                   ServiceListSerializer, ServiceSerializer,
                                   ShowcaseGallerySerializer,
                                   SliderImageSerializer)

message = (
    "Only one item can be created."
    " Please update the existing one."
    " You can also delete existing item to add a new one."
)


class SliderImageViewSet(viewsets.ModelViewSet):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if SliderImage.objects.count() >= 1:
            message = (
                "Only one item can be created."
                " Please update the existing one."
                " You can also delete existing item to add a new one."
            )
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        slider_image = self.get_object()
        slider_image.image.delete()
        return super().destroy(request, *args, **kwargs)


class ShowcaseGalleryViewSet(viewsets.ModelViewSet):
    queryset = ShowcaseGalleryImage.objects.all()
    serializer_class = ShowcaseGallerySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        message = (
            f"Only ${MAX_SHOWCASE_GALLERY_IMAGES} items can be created."
            " Please update the existing one."
            " You can also delete an existing item to add a new one."
        )
        if ShowcaseGalleryImage.objects.count() >= MAX_SHOWCASE_GALLERY_IMAGES:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        showcase_gallery_image = self.get_object()
        showcase_gallery_image.image.delete()
        return super().destroy(request, *args, **kwargs)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ServiceListSerializer
        else:
            return ServiceSerializer

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        service_images = ServiceImage.objects.filter(service=service)
        for img in service_images:
            img.delete()
        return super().destroy(request, *args, **kwargs)


class ServiceImageViewSet(viewsets.ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        service_image = self.get_object()
        service_image.image.delete()
        return super().destroy(request, *args, **kwargs)


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AboutUsListSerializer
        return AboutUsSerializer

    def create(self, request, *args, **kwargs):
        if AboutUs.objects.count() >= 1:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        about_us = self.get_object()
        about_us_images = AboutUsImage.objects.filter(about_us=about_us)
        for img in about_us_images:
            img.delete()
        return super().destroy(request, *args, **kwargs)


class AboutUsImageViewSet(viewsets.ModelViewSet):
    queryset = AboutUsImage.objects.all()
    serializer_class = AboutUsImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        about_us_image = self.get_object()
        about_us_image.image.delete()
        return super().destroy(request, *args, **kwargs)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["writer", "seen"]
    search_fields = ["writer__username", "subject"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FeedbackListSerializer
        else:
            return FeedbackSerializer

    def destroy(self, request, *args, **kwargs):
        feedback = self.get_object()
        feedback_files = FeedbackFile.objects.filter(feedback=feedback)
        for file in feedback_files:
            file.delete()
        return super().destroy(request, *args, **kwargs)


class FeedbackFileViewSet(viewsets.ModelViewSet):
    queryset = FeedbackFile.objects.all()
    serializer_class = AboutUsImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        feedback_file = self.get_object()
        feedback_file.file.delete()
        return super().destroy(request, *args, **kwargs)


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ContactUsListSerializer
        else:
            return ContactUsSerializer

    def create(self, request, *args, **kwargs):
        if ContactUs.objects.count() >= 1:
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
