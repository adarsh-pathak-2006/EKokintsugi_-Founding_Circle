from django.core.management.base import BaseCommand

from pilot.models import PilotUser, PointsAccount, PointTransaction, ReturnRequest, Shoe, SymbolicTree, WeeklyReview


class Command(BaseCommand):
    help = "Seed the pilot system with admin and 10 demo users."

    def handle(self, *args, **options):
        if PilotUser.objects.filter(email="admin@ekokintsugi.com").exists():
            self.stdout.write(self.style.WARNING("Seed data already exists."))
            return

        admin = PilotUser.objects.create_superuser(
            username="pilotadmin",
            email="admin@ekokintsugi.com",
            password="admin123",
            first_name="Pilot",
            last_name="Admin",
        )
        admin.is_staff = True
        admin.save()

        roles = ["intern", "team", "supporter"]
        cities = ["Bengaluru", "Pune", "Mumbai", "Hyderabad", "Delhi"]
        plant_types = ["Neem", "Peepal", "Mango", "Banyan", "Tulsi"]

        for index in range(1, 11):
            role = roles[(index - 1) % len(roles)]
            user = PilotUser.objects.create_user(
                username=f"pilot{index}",
                email=f"pilot{index}@ekokintsugi.com",
                password="pilot123",
                first_name="Pilot",
                last_name=f"User {index}",
                phone=f"98765000{index:02d}",
                role=role,
                city=cities[(index - 1) % len(cities)],
                address=f"{index} Circular Lane, Green District",
                shoe_size=str(5 + (index % 5)),
                start_date=f"2026-05-{index:02d}" if role == "intern" else None,
                end_date=f"2026-07-{index:02d}" if role == "intern" else None,
            )
            Shoe.objects.create(
                user=user,
                shoe_id=f"SHOE-{1000 + index}",
                product_line="Urban Scrap Runner" if index % 2 == 0 else "Kintsugi Street Sole",
                size=user.shoe_size,
                status="Delivered" if index <= 4 else "Pre-booked",
            )
            SymbolicTree.objects.create(
                user=user,
                tree_id=f"TREE-{200 + index}",
                plant_type=plant_types[(index - 1) % len(plant_types)],
                location=f"Community Plot {index}, Eco Campus",
            )
            account = PointsAccount.objects.create(
                user=user,
                total_earned=100 + index * 10,
                approved=80 + index * 5,
                used=30 if index % 3 == 0 else 10,
            )
            PointTransaction.objects.create(account=account, action_type="credit", amount=100 + index * 10, note="Pilot onboarding bonus")

        user1 = PilotUser.objects.get(email="pilot1@ekokintsugi.com")
        user2 = PilotUser.objects.get(email="pilot2@ekokintsugi.com")
        user3 = PilotUser.objects.get(email="pilot3@ekokintsugi.com")

        WeeklyReview.objects.create(
            user=user1,
            week=1,
            days_worn=5,
            hours_per_day=6,
            comfort=4,
            fit=5,
            sole=4,
            material=4,
            stitching=5,
            feedback="Comfortable on daily commute, slight warmth after long walks.",
        )
        WeeklyReview.objects.create(
            user=user2,
            week=1,
            days_worn=4,
            hours_per_day=5,
            comfort=4,
            fit=4,
            sole=4,
            material=5,
            stitching=4,
            feedback="Good grip and fit, material feels strong.",
        )
        ReturnRequest.objects.create(
            user=user3,
            shoe=user3.shoe,
            reason="Pilot period completed",
            condition="Good",
            status="Requested",
        )

        self.stdout.write(self.style.SUCCESS("Seeded admin and 10 pilot users."))
