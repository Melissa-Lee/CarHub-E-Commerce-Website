from django import forms
from .models import DealerProfile

class DealerProfileForm(forms.ModelForm):
    class Meta:
        model = DealerProfile
        fields = ['company_name', 'company_address', 'email', 'phone_number', 'bio', 'contact_info']
