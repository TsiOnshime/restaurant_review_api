from rest_framework import viewsets, permissions
from .models import Restaurant
from reviews.models import Review
from .serializers import RestaurantSerializer
from reviews.serializers import ReviewSerializer

# Handles GET /api/restaurants/ and GET /api/restaurants/<id>/
class RestaurantViewSet(viewsets.ModelViewSet):
    # Allow all users (even unauthenticated) to view restaurants
    permission_classes = [permissions.AllowAny] 
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    # Restrict creation (POST) to authenticated users (or you could restrict it to Admin users only)
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

# Custom View for GET /api/restaurants/<id>/reviews/
from rest_framework.decorators import action
from rest_framework.response import Response

class RestaurantReviewViewSet(viewsets.ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet only supports List and Retrieve (GET)
    permission_classes = [permissions.AllowAny] 
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """List all reviews for a specific restaurant."""
        restaurant = self.get_object()
        reviews = Review.objects.filter(restaurant=restaurant)
        # Use the ReviewSerializer to format the output
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
