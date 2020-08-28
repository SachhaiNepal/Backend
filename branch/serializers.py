from django.contrib.auth import get_user_model
from rest_framework import serializers

from branch.models import Branch

class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"

class BranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
                
    
  