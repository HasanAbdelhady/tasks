from django.core.management.base import BaseCommand
from tasks.models import Task, Subtask

class Command(BaseCommand):
    help = 'Deletes all tasks and their related subtasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion without confirmation',
        )

    def handle(self, *args, **options):
        task_count = Task.objects.count()
        subtask_count = Subtask.objects.count()
        
        if task_count == 0:
            self.stdout.write(self.style.WARNING('No tasks found to delete.'))
            return
            
        if not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    f'This will delete {task_count} tasks and {subtask_count} subtasks.\n'
                    'Are you sure you want to continue? [y/N]: '
                )
            )
            
            if input().lower() != 'y':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Delete all tasks (this will cascade delete subtasks due to ForeignKey relationship)
        Task.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {task_count} tasks and {subtask_count} subtasks.'
            )
        ) 