from django.core.management.base import BaseCommand, CommandError
from portal.sms.sms_daemon import *
class Command(BaseCommand):
    help = 'Initiates the daemon process for sending SMS'

    def handle(self, *args, **options):
        sms_daemon()
