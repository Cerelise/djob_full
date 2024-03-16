import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone

# 自定义用户管理器
class UserAccountManager(BaseUserManager):
    # 创建学生
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
          email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # 创建企业
    def create_employer(self,email,password=None):
        user = self.create_user(email,password)
        user.is_employer = True
        user.save(using=self.db)
        return user
    # 创建管理员
    def create_superuser(self,email,password=None):
        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


# 创建用户模型
class UserAccount(AbstractBaseUser,PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = '男'
        FEMALE = '女'
        NOTSET = '保密'

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatar',null=True,blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices,default=Gender.NOTSET)
    description = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    resume = models.FileField(null=True,blank=True,upload_to='user_resume')
    is_employer = models.BooleanField(default=False)
    objects = UserAccountManager()
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        user_type = None
        if self.is_superuser:
            user_type = '管理员'
        elif self.is_employer:
            user_type = '招聘者'
        else:
            user_type = '普通用户'
        return f'{self.email}_{user_type}'

