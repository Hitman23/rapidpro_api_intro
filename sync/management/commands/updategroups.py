from django.core.management import BaseCommand
from sync.models import Tembarun


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tembarun.get_runs()
        self.stdout.write(self.style.SUCCESS('Successfully run tamba'))

