from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes all non-superuser accounts'

    def handle(self, *args, **options):
        # Delete all users except superusers
        deleted_count = User.objects.filter(is_superuser=False).delete()[0]
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} normal users')
        ) 