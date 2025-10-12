from rest_framework import serializers
from .models import Restaurant
from reviews.serializers import ReviewSerializer # We will define this next

# Used for listing all restaurants and showing restaurant details
class RestaurantSerializer(serializers.ModelSerializer):
    # This field shows all associated reviews when viewing a single restaurant
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        # Note: 'reviews' is included here because we defined related_name='reviews' in the Review model
        fields = ['id', 'name', 'address', 'description', 'reviews']

    def get_reviews(self, obj):
        # Only show the basic review details (ID, rating, comment) when listing
        from reviews.models import Review
        reviews_queryset = Review.objects.filter(restaurant=obj).select_related('user')
        # Return a simplified list of reviews for embedding in the restaurant detail view
        return [{'id': r.id, 'rating': r.rating, 'comment': r.comment, 'user': r.user.username} for r in reviews_queryset]
