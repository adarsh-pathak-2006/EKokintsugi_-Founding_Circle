from django.core.management.base import BaseCommand

from pilot.seed import seed_pilot_data


class Command(BaseCommand):
    help = "Seed the pilot system with admin and 10 demo users."

    def handle(self, *args, **options):
        if seed_pilot_data():
            self.stdout.write(self.style.SUCCESS("Seeded admin and 10 pilot users."))
            return

        self.stdout.write(self.style.WARNING("Seed data already exists."))
