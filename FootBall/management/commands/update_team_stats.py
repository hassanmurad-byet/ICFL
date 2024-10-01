from django.core.management.base import BaseCommand
from FootBall.utils import calculate_team_stats  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Calculate and update team statistics based on finished matches'

    def handle(self, *args, **kwargs):
        calculate_team_stats()
        self.stdout.write(self.style.SUCCESS('Successfully updated team statistics'))