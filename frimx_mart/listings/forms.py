from django import forms
from .models import Listing, ListingImage, Review

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'negotiable', 'category', 'condition', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'negotiable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Price',
            'negotiable': 'Price is negotiable',
            'category': 'Category',
            'condition': 'Condition',
            'location': 'Location',
        }

class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'is_verified_purchase']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_verified_purchase': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'rating': 'Rating (1-5)',
            'comment': 'Review Comment',
            'is_verified_purchase': 'This is a verified purchase',
        }

