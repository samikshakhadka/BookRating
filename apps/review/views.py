from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Opinion, Book
from .serializers import ReviewSerializer, AverageRatingSerializer, TopBookSerializer 
from .filters import OpinionFilter

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Opinion.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OpinionFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], serializer_class= AverageRatingSerializer, permission_classes=[permissions.AllowAny])
    def average_ratings(self, request):
        cache_key = 'average_ratings'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = Book.objects.all()
            serializer = AverageRatingSerializer(queryset, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, timeout=60*1)
        return Response(cached_data)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()