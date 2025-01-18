from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name

class DailyProgress(models.Model):
    date = models.DateField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_subtasks = models.IntegerField(default=0)
    total_subtasks = models.IntegerField(default=0)

    class Meta:
        unique_together = ['date', 'task', 'assignee']

    def __str__(self):
        return f"{self.assignee.username} - {self.task.name} - {self.date}"

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.assignee.username if self.assignee else "Unassigned"}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.assignee:
            # Update daily progress
            today = timezone.now().date()
            daily_progress, created = DailyProgress.objects.get_or_create(
                date=today,
                task=self.task,
                assignee=self.assignee,
                defaults={'total_subtasks': 5}  # Assuming 5 subtasks per task
            )
            
            # Update completed count
            completed_count = Subtask.objects.filter(
                task=self.task,
                assignee=self.assignee,
                completed=True
            ).count()
            daily_progress.completed_subtasks = completed_count
            daily_progress.save()
