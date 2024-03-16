from django_filters import rest_framework as filters

from .models import UserAccount


# 搜索用户时使用的过滤器
class UserFilter(filters.FilterSet):
    # 使用name字段自定义过滤器
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    class Meta:
        model = UserAccount
        fields = ('name')