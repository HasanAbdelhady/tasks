from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Subtask


@receiver(post_save, sender=Task)
def create_subtasks_for_task(sender, instance, created, **kwargs):
    """
    Create 15 default subtasks for each task when it is created.
    """
    if created:
        for i in range(1, 16):  # Create 15 subtasks
            Subtask.objects.create(task=instance, name=f"Subtask {i}")
