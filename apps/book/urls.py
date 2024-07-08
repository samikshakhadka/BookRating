from django.urls import path
from rest_framework import routers

from .views import  BookViewSet
router = routers.DefaultRouter()
router.register(r"", BookViewSet,)
urlpatterns= router.urls
# urlpatterns = [
#     path('books/', BookDetailView.as_view(), name='book-list-create'),
#     path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
#     path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
#     path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
#     # path('books/<int:pk>/soft-delete/', BookSoftDeleteView.as_view(), name='book-soft-delete'),

# ]
