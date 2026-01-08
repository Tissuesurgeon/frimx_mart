from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report
from .forms import ReportForm

@login_required
def create_report(request, user_id=None, listing_id=None):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, 'Report submitted successfully! Our team will review it.')
            return redirect('home')
    else:
        initial = {}
        if user_id:
            from accounts.models import User
            initial['reported_user'] = get_object_or_404(User, id=user_id)
        if listing_id:
            from listings.models import Listing
            initial['listing'] = get_object_or_404(Listing, id=listing_id)
        
        form = ReportForm(initial=initial)
    
    return render(request, 'reports/create_report.html', {'form': form})