from django import forms
from .models import Car, Category, Review, Wishlist

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['dealer', 'make', 'model', 'category', 'year', 'price', 'image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    make = forms.CharField(label='Make', max_length=100, required=False)
    min_price = forms.DecimalField(label='Min Price', max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(label='Max Price', max_digits=10, decimal_places=2, required=False)

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['rating', 'comment']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = []
