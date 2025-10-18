from rest_framework import viewsets, permissions, status
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

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
        user = self.request.user
        restaurant = serializer.validated_data.get('restaurant')
        # prevent multiple reviews by same user for the same restaurant
        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            raise PermissionDenied("You have already reviewed this restaurant.")
        serializer.save(user=user)

    # Override to ensure only the owner can update or delete a review
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()
