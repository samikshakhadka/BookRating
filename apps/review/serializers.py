from rest_framework import serializers
from .models import Opinion
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    #average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Opinion
        fields = ['id', 'book', 'user', 'rating', 'comment']
        read_only_fields = [ 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    # def get_average_rating(self, obj):
    #     avg_rating = Opinion.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
    #     return avg_rating or 0

class AverageRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Opinion
        fields = ['id', 'average_rating']

    def get_average_rating(self, obj):
        avg_rating = Opinion.objects.filter(book=obj).aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0