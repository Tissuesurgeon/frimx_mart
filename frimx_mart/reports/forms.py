from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reported_user', 'listing', 'reason', 'description', 'evidence']
        widgets = {
            'reported_user': forms.Select(attrs={'class': 'form-control'}),
            'listing': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'evidence': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'reported_user': 'Reported User',
            'listing': 'Listing (if applicable)',
            'reason': 'Reason for Report',
            'description': 'Description',
            'evidence': 'Evidence (Optional)',
        }

