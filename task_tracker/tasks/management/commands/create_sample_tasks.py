from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from tasks.models import Task, Subtask


class Command(BaseCommand):
    help = 'Creates sample tasks and subtasks'

    def handle(self, *args, **options):
        # Define main states and actions
        tasks_data = [
            {"name": "تجميع وتحليل البيانات", "minutes_to_deadline": 10},
            {"name": "تطوير واجهة المستخدم", "minutes_to_deadline": 20},
            # Add more tasks as needed
        ]

        for task_data in tasks_data:
            task_deadline = now() + \
                timedelta(minutes=task_data["minutes_to_deadline"])
            task = Task.objects.create(
                name=task_data["name"],
                deadline=task_deadline
            )
            # Create subtasks for each task
            for i in range(5):  # Assuming 5 subtasks per task
                Subtask.objects.create(
                    task=task,
                    name=f"Subtask {i + 1} for {task.name}"
                )

        self.stdout.write(self.style.SUCCESS(
            'Successfully created sample tasks and subtasks'))
