from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg, Q
import uuid

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Seller stats
    total_listings = models.IntegerField(default=0)
    sold_listings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    @property
    def average_rating(self):
        from listings.models import Review
        rating = Review.objects.filter(seller=self).aggregate(Avg('rating'))['rating__avg']
        return rating if rating else 0
    
    @property
    def total_ratings(self):
        from listings.models import Review
        return Review.objects.filter(seller=self).count()
    
    @property
    def unread_messages_count(self):
        from chat.models import Message, ChatThread
        # Count unread messages in threads where user is buyer or seller
        threads = ChatThread.objects.filter(
            Q(buyer=self) | Q(seller=self),
            is_active=True
        )
        return Message.objects.filter(
            thread__in=threads,
            is_read=False
        ).exclude(sender=self).count()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    preferred_contact = models.CharField(
        max_length=20,
        choices=[('email', 'Email'), ('phone', 'Phone'), ('chat', 'In-App Chat')],
        default='chat'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
