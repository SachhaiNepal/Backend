from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet



class BranchViewSet(viewsets.ModelViewSet):
     queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAdminUser]



# Create your views here.
