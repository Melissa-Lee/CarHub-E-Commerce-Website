from django.urls import path
from .views import AddUserFormView, LoginView, LogoutView

app_name = 'authentication'

urlpatterns = [
    path('register/', AddUserFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
