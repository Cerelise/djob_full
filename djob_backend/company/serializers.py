from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    message = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Company
        fields = '__all__'
        