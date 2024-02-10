from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    creation_date = models.DateTimeField(default=timezone.now)  # Set the default value to current timezone
    content = models.TextField()
    subject = models.CharField(max_length=250)
    unread = models.BooleanField(default=True)  

    def __str__(self):
        return f"From: {self.sender}, To: {self.receiver}, Subject: {self.subject}, at: {self.creation_date}"
