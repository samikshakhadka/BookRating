from rest_framework import serializers
from .models import Book, Favorite 
from apps.review.serializers import AverageRatingSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'book']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class BookModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Book
        fields = ['id','title', 'author', 'description', 'average-rating']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user  
        return super().create(validated_data)
    
   