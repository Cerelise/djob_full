from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Job


# 自定义筛选函数
class JobsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category',method="filter_category")
    min_salary = filters.NumberFilter(field_name="salary" or 0, lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="salary" or 1000000, lookup_expr='lte')
    keyword = filters.CharFilter(method='custom_filter',label="search")
    class Meta:
        model = Job
        fields = ('title', 'location', 'min_salary', 'max_salary','keyword','category')

    # 使用工作标签筛选
    def filter_category(self, queryset, name, value):
        categories = value.split(',') # ['JAVA','spring']
        query = Q()
        for category in categories:
            query = query | Q(category__icontains=category)
        return queryset.filter(query)
    # 通过名称、工作地点和薪资筛选
    def custom_filter(self,queryset,name,value):
        return queryset.filter(
          Q(title__icontains=value) | Q(location__icontains=value) 
          | Q(salary__icontains=value) 
        )
