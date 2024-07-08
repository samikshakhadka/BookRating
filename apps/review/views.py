from rest_framework import viewsets, permissions
from .models import Opinion, Book
from .serializers import ReviewSerializer, AverageRatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Opinion.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], serializer_class= AverageRatingSerializer)
    def average_ratings(self, request):
        queryset = Book.objects.all()
        serializer = AverageRatingSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()