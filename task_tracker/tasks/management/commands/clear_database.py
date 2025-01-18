from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task, Subtask, DailyProgress

class Command(BaseCommand):
    help = 'Clears all data from the database except superusers'

    def handle(self, *args, **options):
        # Delete all tasks (this will cascade delete subtasks)
        tasks_deleted = Task.objects.all().delete()[0]
        
        # Delete all daily progress records
        progress_deleted = DailyProgress.objects.all().delete()[0]
        
        # Delete all non-superuser accounts
        users_deleted = User.objects.filter(is_superuser=False).delete()[0]

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleared database:\n'
                f'- {tasks_deleted} tasks (and their subtasks) deleted\n'
                f'- {progress_deleted} daily progress records deleted\n'
                f'- {users_deleted} normal users deleted\n'
                f'Superuser(s) retained.'
            )
        ) 