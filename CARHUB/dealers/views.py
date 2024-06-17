from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import DealerProfile
from cars.models import Car, Wishlist
from authentication.models import UserProfile
from .forms import DealerProfileForm
from django.http import HttpResponseNotFound

def is_dealer(user):
    return user.userprofile.user_type == 'dealer'

def is_customer(user):
    return user.userprofile.user_type == 'customer'

def dealer_list(request):
    dealers = DealerProfile.objects.all()
    return render(request, 'dealers/dealer_list.html', {'dealers': dealers})

def dealer_profile(request, dealer_id):
    dealer_profile = get_object_or_404(DealerProfile, id=dealer_id)
    cars = dealer_profile.get_cars()
    wishlist_counts = {car.id: dealer_profile.get_wishlist_count(car) for car in cars}
    return render(request, 'dealers/dealer_profile.html', {'dealer_profile': dealer_profile, 'cars': cars, 'wishlist_counts': wishlist_counts})

@login_required
@user_passes_test(is_dealer)
def manage_cars(request):
    try:
        dealer_profile = DealerProfile.objects.get(user=request.user.userprofile)
    except DealerProfile.DoesNotExist:
        return redirect('dealers:update_profile')  # Redirect to profile update if not found
    
    cars = Car.objects.filter(dealer=request.user.userprofile)
    for car in cars:
        car.wishlist_count = car.wishlist_count()
    
    return render(request, 'dealers/manage_cars.html', {'dealer_profile': dealer_profile, 'cars': cars})

@login_required
@user_passes_test(is_dealer)
def update_profile(request):
    try:
        dealer_profile = DealerProfile.objects.get(user=request.user.userprofile)
    except DealerProfile.DoesNotExist:
        dealer_profile = DealerProfile(user=request.user.userprofile)
    
    if request.method == 'POST':
        form = DealerProfileForm(request.POST, instance=dealer_profile)
        if form.is_valid():
            form.save()
            return redirect('dealers:manage_cars')
    else:
        form = DealerProfileForm(instance=dealer_profile)
    return render(request, 'dealers/update_profile.html', {'form': form})

