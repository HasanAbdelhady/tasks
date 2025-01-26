from django.db import models
from django.contrib.auth.models import User
from tasks.models import Subtask

RANK_TO_SUBTASK_INDEX = {
    'Private': 0,
    'Corporal': 1,
    'Sergeant': 2,
    'Staff Sergeant': 3,
    'Warrant Officer': 4,
    'Second Lieutenant': 5,
    'First Lieutenant': 6,
    'Captain': 7,
    'Major': 8,
    'Lieutenant Colonel': 9,
    'Colonel': 10,
    'Brigadier General': 11,
    'Major General': 12,
    'Lieutenant General': 13,
    'General': 14,
}


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    rank = models.CharField(max_length=50)
    subtask = models.ForeignKey(
        Subtask, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.rank}"

    def assign_subtask(self):
        """
        Assigns the subtask to the user based on their rank.
        """
        index = RANK_TO_SUBTASK_INDEX.get(self.rank)
        if index is not None:
            subtasks = Subtask.objects.filter(
                task__isnull=False  # Ensure subtasks belong to a task
            ).order_by('task', 'id')  # Ordered by task and subtask order

            if index < len(subtasks):
                self.subtask = subtasks[index]
                self.subtask.assignee = self.user
                self.subtask.save()
                self.save()
