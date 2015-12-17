from django.core.management.base import BaseCommand, CommandError
from dummy_db import script
class Command(BaseCommand):
    help = 'Initiates the daemon process for sending SMS'

    def handle(self, *args, **options):
        script.main()
