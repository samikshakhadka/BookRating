from django.db.models import Avg
from rest_framework import serializers

from .models import Opinion, Book



class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Opinion
        fields = ['id', 'book', 'rating', 'comment']
        read_only_fields = [ 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AverageRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Opinion
        fields = ['id', 'average_rating']

    def get_average_rating(self, obj):
        avg_rating = Opinion.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0
    

class TopBookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'average_rating']

    def get_average_rating(self, obj):
        avg_rating = Opinion.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0