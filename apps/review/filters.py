from django_filters import rest_framework as filters
from .models import Opinion

class OpinionFilter(filters.FilterSet):
    book = filters.NumberFilter(field_name='book__id')
    user = filters.NumberFilter(field_name='user__id')
    rating = filters.RangeFilter()
    comment = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Opinion
        fields = ['book', 'user', 'rating', 'comment', 'created_at']
