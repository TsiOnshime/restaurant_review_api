from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# Handles all CRUD operations for reviews: GET, POST, PUT, DELETE /api/reviews/
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('user', 'restaurant').all()
    # Only authenticated users can interact with reviews (Create, Update, Delete)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        """Optionally restricts the returned reviews to a given user, or all for staff."""
        # This implementation allows all users to read all reviews for the list endpoint
        return Review.objects.all().select_related('user', 'restaurant')

    # Override to automatically set the user when a review is created (POST)
    def perform_create(self, serializer):
        # Before saving, check if the user has already reviewed this restaurant
        restaurant_id = serializer.validated_data.get('restaurant').id
        if Review.objects.filter(user=self.request.user, restaurant_id=restaurant_id).exists():
            raise PermissionDenied("You have already submitted a review for this restaurant.")
        
        # Save the new review, automatically setting the user field to the logged-in user
        serializer.save(user=self.request.user)

    # Override to ensure only the owner can update or delete a review
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review.")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()
