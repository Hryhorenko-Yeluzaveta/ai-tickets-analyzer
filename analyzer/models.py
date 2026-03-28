from django.db import models

class Ticket(models.Model):
    author_email = models.CharField(max_length=100)
    message = models.TextField()