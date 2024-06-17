from django.db import models
from authentication.models import UserProfile
from cars.models import Car

class DealerProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='dealer_profile')
    company_name = models.CharField(max_length=100)
    company_address = models.TextField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    def get_cars(self):
        return Car.objects.filter(dealer=self.user)

    def get_wishlist_count(self, car):
        return car.wishlist_set.count()
