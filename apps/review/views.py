from django.db.models import Avg

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Opinion, Book
from .serializers import ReviewSerializer, AverageRatingSerializer, TopBookSerializer 


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Opinion.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], serializer_class= AverageRatingSerializer, permission_classes=[permissions.AllowAny])
    def average_ratings(self, request):
        queryset = Book.objects.all()
        serializer = AverageRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()