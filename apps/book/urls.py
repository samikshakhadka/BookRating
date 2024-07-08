from django.urls import path
from rest_framework import routers

from .views import  BookViewSet

router = routers.DefaultRouter()
router.register(r"", BookViewSet,)
urlpatterns= router.urls

