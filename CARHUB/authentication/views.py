from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from .models import UserProfile
from dealers.models import DealerProfile
from django.db import transaction, IntegrityError
import logging

logger = logging.getLogger(__name__)

class AddUserFormView(View):
    template_name = 'authentication/register.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password1']
                    user_type = form.cleaned_data['user_type']
                    user.set_password(password)
                    user.save()

                    # Create UserProfile
                    user_profile, created = UserProfile.objects.get_or_create(user=user, defaults={'user_type': user_type})

                    # Update user_type if the profile already exists
                    if not created:
                        user_profile.user_type = user_type
                        user_profile.save()

                    # Create DealerProfile if the user is a dealer
                    if user_type == 'dealer':
                        DealerProfile.objects.get_or_create(user=user_profile)

                    messages.success(request, 'Registration successful. Please log in.')
                    return redirect('authentication:login')

            except IntegrityError as e:
                logger.error(f"Integrity error during user registration: {e}")
                messages.error(request, 'A user with that username or email already exists.')
            except Exception as e:
                logger.error(f"Unexpected error during user registration: {e}")
                messages.error(request, 'An unexpected error occurred during registration. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below')

        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        next_url = request.POST.get('next', request.GET.get('next', ''))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    url = '/'

    def get(self, request):
        logout(request)
        return redirect(self.url)
