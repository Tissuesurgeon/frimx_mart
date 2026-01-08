from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

REPORT_REASONS = [
    ('spam', 'Spam'),
    ('fraud', 'Fraud or Scam'),
    ('offensive', 'Offensive Content'),
    ('inappropriate', 'Inappropriate Item'),
    ('fake', 'Fake Item'),
    ('harassment', 'Harassment'),
    ('other', 'Other'),
]

REPORT_STATUS = [
    ('pending', 'Pending'),
    ('investigating', 'Investigating'),
    ('resolved', 'Resolved'),
    ('dismissed', 'Dismissed'),
]

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received', null=True, blank=True)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=50, choices=REPORT_REASONS)
    description = models.TextField()
    evidence = models.FileField(upload_to='report_evidence/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_reports')
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reporter} on {self.created_at}"
    
    def mark_resolved(self, user, notes=""):
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolved_by = user
        self.resolution_notes = notes
        self.save()