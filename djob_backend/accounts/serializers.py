from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80,required=True)
    password = serializers.CharField(min_length=8, write_only=True,required=True)
    is_employer = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['email','password','is_employer']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("该邮箱已被使用！")
        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='is_superuser',read_only=True)
    avatar = serializers.ImageField(required=False,read_only=True)
    resume = serializers.FileField(required=False,read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = User
        fields = ('id','name', 'email', 'is_employer','phone','description','avatar','gender','resume','is_admin','password','date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False,read_only=True)
    avatar = serializers.ImageField(required=False,read_only=True)
    resume = serializers.FileField(required=False,read_only=True)
    phone = serializers.CharField(required=False,allow_blank=True)
    description = serializers.CharField(required=False,allow_blank=True)
    is_employer = serializers.BooleanField(required=False,read_only=True)
    
    class Meta:
        model = User
        fields = ('id','email','name','phone','description','avatar','gender','resume','is_employer')