from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    message = serializers.CharField(required=False)
    class Meta:
        model = Company
        fields = '__all__'
        