from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cars.models import Car, Wishlist, Review
from authentication.models import UserProfile

@login_required
def index(request):
    user_profile = request.user.userprofile

    if user_profile.user_type == 'dealer':
        cars = Car.objects.filter(dealer=user_profile)
        total_cars = cars.count()
        total_wishlists = Wishlist.objects.filter(car__in=cars).count()
        recent_reviews = Review.objects.filter(car__in=cars).order_by('-created_at')[:5]
        context = {
            'total_cars': total_cars,
            'total_wishlists': total_wishlists,
            'recent_reviews': recent_reviews
        }
    else:
        wishlist_items = Wishlist.objects.filter(user=user_profile)
        latest_reviews = Review.objects.filter(user=user_profile).order_by('-created_at')[:5]
        context = {
            'wishlist_items': wishlist_items,
            'latest_reviews': latest_reviews
        }
    
    return render(request, 'index.html', context)
