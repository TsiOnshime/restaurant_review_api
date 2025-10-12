from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    # Read-only field to show the username instead of the user ID
    user = serializers.ReadOnlyField(source='user.username')
    
    # Read-only field to show the restaurant name
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'restaurant_name', 'user', 'rating', 'comment', 'created_at']
        # The 'user' field is omitted from fields and handled automatically in the ViewSet

    # Custom Validation to enforce the rating must be between 1 and 5
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
