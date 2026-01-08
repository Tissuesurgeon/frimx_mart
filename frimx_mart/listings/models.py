from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

CATEGORY_CHOICES = [
    ('fashion', '👕 Fashion'),
    ('electronics', '📱 Electronics'),
    ('home_garden', '🏠 Home & Garden'),
    ('vehicles', '🚗 Vehicles'),
    ('property', '🏡 Property'),
    ('services', '🛠️ Services'),
    ('jobs', '💼 Jobs'),
    ('education', '🎓 Education'),
    ('sports', '⚽ Sports'),
    ('books', '📚 Books'),
    ('other', '📦 Other'),
]

CONDITION_CHOICES = [
    ('new', 'New'),
    ('used_like_new', 'Used - Like New'),
    ('used_good', 'Used - Good'),
    ('used_fair', 'Used - Fair'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=20, default='📦')
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    @property
    def listing_count(self):
        return self.listing_set.filter(is_active=True).count()

class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiable = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used_good')
    location = models.CharField(max_length=200)
    
    # Status flags
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    is_boosted = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    boosted_until = models.DateTimeField(null=True, blank=True)
    
    # Counters
    views = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'is_sold']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_boosted_active(self):
        if self.is_boosted and self.boosted_until:
            return self.boosted_until > timezone.now()
        return False

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary image per listing
            ListingImage.objects.filter(listing=self.listing, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'listing']

class Review(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['seller', 'buyer', 'listing']

class Promotion(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    promotion_type = models.CharField(
        max_length=20,
        choices=[('boost', 'Boost'), ('featured', 'Featured'), ('urgent', 'Urgent')]
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)