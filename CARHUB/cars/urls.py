from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('showroom/', views.showroom, name='showroom'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('car/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('car/add/', views.add_car, name='add_car'),
    path('car/update/<int:car_id>/', views.update_car, name='update_car'),
    path('car/delete/<int:pk>/', views.delete_car, name='delete_car'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
