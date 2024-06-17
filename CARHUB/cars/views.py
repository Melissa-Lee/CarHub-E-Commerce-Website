from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Car, Category, Wishlist, Review
from authentication.models import UserProfile
from .forms import CarForm, SearchForm, ReviewForm, WishlistForm

def is_dealer(user):
    return user.userprofile.user_type == 'dealer'

def is_customer(user):
    return user.userprofile.user_type == 'customer'

def showroom(request):
    cars = Car.objects.all()
    categories = Category.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        make = form.cleaned_data.get('make')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if query:
            cars = cars.filter(Q(make__icontains=query) | Q(model__icontains=query))
        if category:
            cars = cars.filter(category=category)
        if make:
            cars = cars.filter(make__icontains=make)
        if min_price is not None:
            cars = cars.filter(price__gte=min_price)
        if max_price is not None:
            cars = cars.filter(price__lte=max_price)

    return render(request, 'cars/showroom.html', {'cars': cars, 'categories': categories, 'form': form})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    if request.method == 'POST':
        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.car = car
                review.user = UserProfile.objects.get(user=request.user)
                review.save()
                messages.success(request, 'Review added successfully!')
                return redirect('cars:car_detail', car_id=car.id)
        elif 'wishlist_submit' in request.POST:
            wishlist_form = WishlistForm(request.POST)
            if wishlist_form.is_valid():
                wishlist = wishlist_form.save(commit=False)
                wishlist.user = UserProfile.objects.get(user=request.user)
                wishlist.car = car
                wishlist.save()
                messages.success(request, 'Car added to wishlist!')
                return redirect('cars:car_detail', car_id=car.id)
    else:
        review_form = ReviewForm()
        wishlist_form = WishlistForm()

    return render(request, 'cars/car_detail.html', {'car': car, 'reviews': reviews, 'review_form': review_form, 'wishlist_form': wishlist_form})

@login_required
@user_passes_test(is_dealer)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.dealer = UserProfile.objects.get(user=request.user)
            car.save()
            return redirect('cars:showroom')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@login_required
@user_passes_test(is_dealer)
def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cars:car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/update_car.html', {'form': form, 'car': car})

@login_required
@user_passes_test(is_dealer)
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if not request.user.userprofile == car.dealer:
        return HttpResponseForbidden()
    if request.method == 'POST':
        car.delete()
        return redirect('cars:showroom')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})

@login_required
@user_passes_test(is_customer)
def wishlist(request):
    user_profile = UserProfile.objects.get(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=user_profile)
    return render(request, 'cars/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
@user_passes_test(is_customer)
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=UserProfile.objects.get(user=request.user), car=car)
    if created:
        messages.success(request, 'Car added to wishlist!')
    else:
        messages.info(request, 'Car is already in your wishlist.')
    return redirect('cars:car_detail', car_id=car_id)

@login_required
@user_passes_test(is_customer)
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = UserProfile.objects.get(user=request.user)
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('cars:car_detail', car_id=car.id)
    else:
        form = ReviewForm()
    return render(request, 'cars/add_review.html', {'car': car, 'form': form})
