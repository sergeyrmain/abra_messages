from django.db import models

from messages.enums.status import Status


class NotDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status=Status.DELETED)


class NonDeletableModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = Status.ACTIVE
        DELETED = Status.DELETED

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)

    objects = NotDeletedManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.status = self.StatusChoices.DELETED
        self.save()

    class Meta:
        abstract = True

