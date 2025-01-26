from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Task: {self.task.name})"

    def confirm_completion(self):
        self.completed = True
        self.save()


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
