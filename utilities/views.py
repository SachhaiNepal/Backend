from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utilities.models import (AboutUs, AboutUsImage, Service, ShowcaseGalleryImage,
                              SliderImage)
from utilities.serializers import (AboutUsImageSerializer,
                                   AboutUsListSerializer, AboutUsSerializer,
                                   ServiceSerializer,
                                   ShowcaseGallerySerializer,
                                   ShowcaseSliderSerializer)


class ShowcaseSliderViewSet(viewsets.ModelViewSet):
    queryset = SliderImage.objects.all()
    serializer_class = ShowcaseSliderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if SliderImage.objects.count() >= 3:
            return Response(
                {"message": "More than {} slider images cant be registered.".format(3)}
            )
        return super(ShowcaseSliderViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        slider_image = self.get_object()
        slider_image.image.delete()
        slider_image.delete()
        return Response(
            {"message": "Showcase slider image deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ShowcaseGalleryViewSet(viewsets.ModelViewSet):
    queryset = ShowcaseGalleryImage.objects.all()
    serializer_class = ShowcaseGallerySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if SliderImage.objects.count() >= 3:
            return Response(
                {"message": "More than {} gallery images cant be registered.".format(3)}
            )
        return super(ShowcaseGalleryViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        showcase_gallery_image = self.get_object()
        showcase_gallery_image.image.delete()
        showcase_gallery_image.delete()
        return Response(
            {"message": "Showcase gallery image deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        service.image.delete()
        service.delete()
        return Response(
            {"message": "Service deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AboutUsListSerializer
        return super(AboutUsViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        if AboutUs.objects.count() >= 1:
            return Response(
                {"message": "More than {} gallery images cant be registered.".format(1)}
            )
        return super(AboutUsViewSet, self).create(request, *args, **kwargs)


class AboutUsImageViewSet(viewsets.ModelViewSet):
    queryset = AboutUsImage.objects.all()
    serializer_class = AboutUsImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        about_us_image = self.get_object()
        about_us_image.image.delete()
        about_us_image.delete()
        return Response(
            {"message": "About us image deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
