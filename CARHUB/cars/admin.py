# cars/admin.py

from django.contrib import admin
from .models import Car, Category, Review, Wishlist


admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Wishlist)
