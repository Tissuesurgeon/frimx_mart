from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from listings.models import Listing, Category
from chat.models import ChatThread, Message
from reports.models import Report

@login_required
def user_dashboard(request):
    user = request.user
    
    # User stats
    active_listings = user.listings.filter(is_active=True, is_sold=False).count()
    sold_listings = user.listings.filter(is_sold=True).count()
    total_revenue = user.listings.filter(is_sold=True).aggregate(
        total=Sum('price')
    )['total'] or 0
    
    # Recent activity
    recent_listings = user.listings.order_by('-created_at')[:5]
    recent_chats = ChatThread.objects.filter(
        Q(buyer=user) | Q(seller=user)
    ).order_by('-updated_at')[:5]
    
    # Saved listings
    saved_listings = user.saved_listings.all().select_related('listing')[:5]
    
    context = {
        'active_listings': active_listings,
        'sold_listings': sold_listings,
        'total_revenue': total_revenue,
        'recent_listings': recent_listings,
        'recent_chats': recent_chats,
        'saved_listings': saved_listings,
    }
    return render(request, 'dashboard/user_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Platform stats
    total_users = User.objects.count()
    new_users_today = User.objects.filter(
        date_joined__date=timezone.now().date()
    ).count()
    
    total_listings = Listing.objects.count()
    active_listings = Listing.objects.filter(is_active=True, is_sold=False).count()
    boosted_listings = Listing.objects.filter(
        is_boosted=True,
        boosted_until__gt=timezone.now()
    ).count()
    
    total_chats = ChatThread.objects.count()
    active_chats = ChatThread.objects.filter(is_active=True).count()
    total_messages = Message.objects.count()
    
    # Revenue stats
    total_revenue = 10000  # Placeholder - implement actual revenue tracking
    today_revenue = 500    # Placeholder
    
    # Recent reports
    pending_reports = Report.objects.filter(status='pending').order_by('-created_at')[:10]
    
    # Recent listings for moderation
    recent_listings = Listing.objects.filter(is_active=True).order_by('-created_at')[:10]
    
    # Category distribution
    category_stats = Category.objects.annotate(
        listing_count=Count('listing')
    ).order_by('-listing_count')[:10]
    
    context = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_listings': total_listings,
        'active_listings': active_listings,
        'boosted_listings': boosted_listings,
        'total_chats': total_chats,
        'active_chats': active_chats,
        'total_messages': total_messages,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'pending_reports': pending_reports,
        'recent_listings': recent_listings,
        'category_stats': category_stats,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    
    # Filters
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    context = {
        'users': users,
    }
    return render(request, 'dashboard/manage_users.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def moderate_listings(request):
    listings = Listing.objects.all().order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    if status == 'active':
        listings = listings.filter(is_active=True, is_sold=False)
    elif status == 'sold':
        listings = listings.filter(is_sold=True)
    elif status == 'inactive':
        listings = listings.filter(is_active=False)
    elif status == 'pending':
        listings = listings.filter(is_active=True, is_boosted=False)
    
    context = {
        'listings': listings,
    }
    return render(request, 'dashboard/moderate_listings.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_boost(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        listing.is_boosted = True
        listing.boosted_until = timezone.now() + timedelta(days=7)
        listing.save()
        messages.success(request, 'Listing boost approved!')
        return redirect('moderate_listings')
    
    return render(request, 'dashboard/approve_boost.html', {'listing': listing})