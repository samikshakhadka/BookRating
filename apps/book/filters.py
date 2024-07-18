from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    created_by = filters.NumberFilter(field_name='created_by__id')
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    user = filters.NumberFilter(method= 'filter_by_user')

    def filter_by_user(self, queryset,name,value):
        return queryset.filter(created_by__id=value)

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'created_by', 'created_at', 'updated_at']
