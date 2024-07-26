from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Favorite
from .serializers import BookModelSerializer
from .permissions import IsOwner
from .filters import BookFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_deleted=False)
    serializer_class = BookModelSerializer # NOTE use BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        instance.is_deleted=True
        instance.save(update_fields=['is_deleted'])
        
    
    # def save(self, *args, **kwargs):
    #     updated_fields = kwargs.pop('updated_fields', None)
    #     super().save(*args, **kwargs)
    #     if updated_fields:
    #         # Custom logic to handle updated_fields if needed
    #         pass
    
    # def perform_destroy(self, instance):
    #     instance.is_deleted = True
    #     instance.save(updated_fields=['is_deleted']) 

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        book = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        if created:
            return Response({'status': 'Book marked as favorite'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'Book already marked as favorite'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfavorite(self, request, pk=None):
        book = self.get_object()
        try:
            favorite = Favorite.objects.get(user=request.user, book=book)
            favorite.delete()
            return Response({'status': 'Book unmarked as favorite'}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({'status': 'Book was not marked as favorite'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def list_favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        books = [favorite.book for favorite in favorites]
        serializer = BookModelSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return super().get_permissions()