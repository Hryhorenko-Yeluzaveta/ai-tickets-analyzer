from django.db import models

class Ticket(models.Model):
    URGENCY_CHOICES = {
        'H': 'High',
        'M': 'Medium',
        'L': 'Low',
    }

    SENTIMENT_CHOICES = {
        'POS': 'Positive',
        'NEG': 'Negative',
        'NEU': 'Neutral',
    }

    STATUS_CHOICES = {
        'N': 'New',
        'D': 'Done',
        'P': 'In Progress',
        'R': 'Rejected',
    }

    author_email = models.EmailField(max_length=100)
    message = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    urgency = models.CharField(choices=URGENCY_CHOICES, max_length=1, blank=True, null=True)
    sentiment = models.CharField(choices=SENTIMENT_CHOICES, max_length=3, blank=True, null=True)
    ai_response = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='N')