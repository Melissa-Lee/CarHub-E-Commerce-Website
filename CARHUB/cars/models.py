from django.db import models
from authentication.models import UserProfile


# Create your models here.
class Category(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    HATCHBACK = 'Hatchback'
    COUPE = 'Coupe'
    CONVERTIBLE = 'Convertible'

    CATEGORY_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (HATCHBACK, 'Hatchback'),
        (COUPE, 'Coupe'),
        (CONVERTIBLE, 'Convertible'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=SEDAN)

    def __str__(self):
        return self.name

class Car(models.Model):
    dealer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def wishlist_count(self):
        return self.wishlist_set.count()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.user.username} on {self.car}"

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.username} wishlist - {self.car.make} {self.car.model}"