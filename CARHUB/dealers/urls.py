from django.urls import path
from . import views

app_name = 'dealers'

urlpatterns = [
    path('', views.dealer_list, name='dealer_list'),
    path('<int:dealer_id>/', views.dealer_profile, name='dealer_profile'),
    path('manage/', views.manage_cars, name='manage_cars'),
    path('profile/', views.update_profile, name='update_profile'),
]
