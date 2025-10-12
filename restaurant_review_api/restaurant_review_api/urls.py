"""
URL configuration for restaurant_review_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.views import RestaurantViewSet, RestaurantReviewViewSet
from reviews.views import ReviewViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'reviews', ReviewViewSet, basename='review')
# Note: We are using RestaurantViewSet for listing and retrieving restaurants
# The custom reviews view for a restaurant can be accessed via an @action decorator or a separate route.

urlpatterns = [
    path('admin/', admin.site.urls),
    # DRF browsable API and authentication endpoints
    path('api-auth/', include('rest_framework.urls')),
    
    # User Endpoints (Placeholder - you need a library like djoser or simple-jwt here)
    # Example: path('auth/', include('djoser.urls')),
    # Example: path('auth/', include('djoser.urls.authtoken')),

    # Our core API routes
    path('api/', include(router.urls)),
    
    # Custom Review List route (using the action defined in RestaurantReviewViewSet)
    path('api/restaurants/<int:pk>/reviews/', RestaurantReviewViewSet.as_view({'get': 'reviews'}), name='restaurant-reviews'),
]
