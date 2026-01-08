from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Listing, Category, SavedListing, ListingImage, Review, CONDITION_CHOICES
from .forms import ListingForm, ListingImageForm, ReviewForm
from chat.models import ChatThread

User = get_user_model()

def home(request):
    # Get featured listings
    featured_listings = Listing.objects.filter(
        is_active=True, 
        is_sold=False,
        is_featured=True
    ).order_by('-created_at')[:8]
    
    # Get recent listings
    recent_listings = Listing.objects.filter(
        is_active=True, 
        is_sold=False
    ).order_by('-created_at')[:12]
    
    # Get boosted listings
    boosted_listings = Listing.objects.filter(
        is_active=True,
        is_sold=False,
        is_boosted=True,
        boosted_until__gt=timezone.now()
    ).order_by('-boosted_until')[:6]
    
    # Get categories with most listings
    # Note: We use total_count for ordering, but template will use the property listing_count
    popular_categories = Category.objects.annotate(
        total_count=Count('listing')
    ).order_by('-total_count')[:8]
    
    context = {
        'featured_listings': featured_listings,
        'recent_listings': recent_listings,
        'boosted_listings': boosted_listings,
        'popular_categories': popular_categories,
    }
    return render(request, 'listings/home.html', context)

def listing_list(request):
    listings = Listing.objects.filter(is_active=True, is_sold=False)
    
    # Filters
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    location = request.GET.get('location')
    search = request.GET.get('search')
    sort = request.GET.get('sort', '-created_at')
    
    if category:
        listings = listings.filter(category__name=category)
    if condition:
        listings = listings.filter(condition=condition)
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if location:
        listings = listings.filter(location__icontains=location)
    if search:
        listings = listings.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    # Sorting
    if sort == 'price_asc':
        listings = listings.order_by('price')
    elif sort == 'price_desc':
        listings = listings.order_by('-price')
    elif sort == 'recent':
        listings = listings.order_by('-created_at')
    elif sort == 'popular':
        listings = listings.order_by('-views')
    
    # Pagination
    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'conditions': CONDITION_CHOICES,
        'filters': {
            'category': category,
            'condition': condition,
            'min_price': min_price,
            'max_price': max_price,
            'location': location,
            'search': search,
            'sort': sort,
        }
    }
    return render(request, 'listings/listing_list.html', context)

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    
    # Increment view count
    listing.views += 1
    listing.save()
    
    # Check if user has saved this listing
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(
            user=request.user, 
            listing=listing
        ).exists()
        
        # Check if user has an existing chat with seller
        existing_chat = ChatThread.objects.filter(
            listing=listing,
            buyer=request.user,
            seller=listing.seller
        ).first()
    
    # Get similar listings
    similar_listings = Listing.objects.filter(
        category=listing.category,
        is_active=True,
        is_sold=False
    ).exclude(id=listing.id).order_by('?')[:4]
    
    # Get seller's other listings
    seller_listings = Listing.objects.filter(
        seller=listing.seller,
        is_active=True,
        is_sold=False
    ).exclude(id=listing.id).order_by('-created_at')[:3]
    
    # Get reviews for seller
    seller_reviews = Review.objects.filter(seller=listing.seller).order_by('-created_at')[:5]
    
    context = {
        'listing': listing,
        'is_saved': is_saved,
        'similar_listings': similar_listings,
        'seller_listings': seller_listings,
        'seller_reviews': seller_reviews,
        'existing_chat': existing_chat if request.user.is_authenticated else None,
    }
    return render(request, 'listings/listing_detail.html', context)

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            for i, image in enumerate(images[:8]):  # Limit to 8 images
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_primary=(i == 0)
                )
            
            messages.success(request, 'Listing created successfully!')
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ListingForm()
    
    return render(request, 'listings/create_listing.html', {'form': form})

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'listings/edit_listing.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)
    if request.method == 'POST':
        listing.is_active = False
        listing.save()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'listings/delete_listing.html', {'listing': listing})

@login_required
def mark_as_sold(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)
    if request.method == 'POST':
        listing.is_sold = True
        listing.save()
        messages.success(request, 'Listing marked as sold!')
        return redirect('dashboard')
    
    return render(request, 'listings/mark_sold.html', {'listing': listing})

@login_required
def save_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        saved_listing, created = SavedListing.objects.get_or_create(
            user=request.user,
            listing=listing
        )
        
        if created:
            listing.saves += 1
            listing.save()
            messages.success(request, 'Listing saved to your favorites!')
        else:
            saved_listing.delete()
            listing.saves -= 1
            listing.save()
            messages.success(request, 'Listing removed from favorites.')
    
    return redirect('listing_detail', listing_id=listing_id)

@login_required
def create_review(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.buyer = request.user
            review.seller = seller
            review.save()
            messages.success(request, 'Review submitted successfully!')
            # Redirect to seller's profile - using profile view for the seller
            return redirect('profile')
    else:
        form = ReviewForm()
    
    return render(request, 'listings/create_review.html', {'form': form, 'seller': seller})