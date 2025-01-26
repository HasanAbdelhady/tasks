from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from tasks.models import Subtask


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile for the new User.
    """
    if created:
        # Ensure a UserProfile doesn't already exist
        if not UserProfile.objects.filter(user=instance).exists():
            UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def assign_subtask_based_on_rank(sender, instance, created, **kwargs):
    """
    Assign a subtask to the user based on their rank when UserProfile is created.
    """
    if created:
        rank_to_subtask = {
            'Private': 'Subtask 1',
            'Corporal': 'Subtask 2',
            'Sergeant': 'Subtask 3',
            'Staff Sergeant': 'Subtask 4',
            'Warrant Officer': 'Subtask 5',
            'Second Lieutenant': 'Subtask 6',
            'First Lieutenant': 'Subtask 7',
            'Captain': 'Subtask 8',
            'Major': 'Subtask 9',
            'Lieutenant Colonel': 'Subtask 10',
            'Colonel': 'Subtask 11',
            'Brigadier General': 'Subtask 12',
            'Major General': 'Subtask 13',
            'Lieutenant General': 'Subtask 14',
            'General': 'Subtask 15',
        }

        # Get the subtask for the user's rank
        subtask_name = rank_to_subtask.get(instance.rank)
        if subtask_name:
            subtask = Subtask.objects.filter(name=subtask_name).first()
            if subtask and subtask.assignee is None:  # Only assign if unassigned
                subtask.assignee = instance.user
                subtask.save()
