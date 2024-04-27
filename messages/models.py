from django.db import models
from django.contrib.auth.models import User

from messages.NonDeletableModel import NonDeletableModel
from messages.enums.status import Status


class Message(NonDeletableModel):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=NonDeletableModel.StatusChoices.choices, default=Status.ACTIVE)

