from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Job


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

    
    def filter_category(self, queryset, name, value):
        categories = value.split(',') # ['JAVA','spring']
        query = Q()
        for category in categories:
            # query |= Q(category__icontains=category)
            query = query | Q(category__icontains=category)
            # print(query)
        return queryset.filter(query)

    def custom_filter(self,queryset,name,value):
        
        return queryset.filter(
          Q(title__icontains=value) | Q(location__icontains=value) 
          | Q(salary__icontains=value) 
        )
