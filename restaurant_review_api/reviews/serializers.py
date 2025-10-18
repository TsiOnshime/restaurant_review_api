from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'restaurant_name', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
