from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class ChatThread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chats')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['listing', 'buyer', 'seller']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat: {self.buyer} - {self.seller}"
    
    @property
    def last_message(self):
        return self.messages.order_by('-sent_at').first()
    
    def unread_count(self, user):
        """Return count of unread messages for the given user"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()
    
    def has_unread(self, user):
        """Check if there are unread messages for the given user"""
        return self.messages.filter(is_read=False).exclude(sender=user).exists()

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message from {self.sender}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['blocker', 'blocked']
    
    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"