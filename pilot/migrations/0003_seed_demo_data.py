from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_demo_data(apps, schema_editor):
    PilotUser = apps.get_model("pilot", "PilotUser")
    Shoe = apps.get_model("pilot", "Shoe")
    SymbolicTree = apps.get_model("pilot", "SymbolicTree")
    PointsAccount = apps.get_model("pilot", "PointsAccount")
    PointTransaction = apps.get_model("pilot", "PointTransaction")
    WeeklyReview = apps.get_model("pilot", "WeeklyReview")
    ReturnRequest = apps.get_model("pilot", "ReturnRequest")

    admin, admin_created = PilotUser.objects.get_or_create(
        email="admin@ekokintsugi.com",
        defaults={
            "username": "pilotadmin",
            "first_name": "Pilot",
            "last_name": "Admin",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if admin_created:
        admin.password = make_password("admin123")
        admin.save(update_fields=["password"])
    elif not admin.is_superuser or not admin.is_staff:
        admin.is_superuser = True
        admin.is_staff = True
        admin.save(update_fields=["is_superuser", "is_staff"])

    roles = ["intern", "team", "supporter"]
    cities = ["Bengaluru", "Pune", "Mumbai", "Hyderabad", "Delhi"]
    plant_types = ["Neem", "Peepal", "Mango", "Banyan", "Tulsi"]

    for index in range(1, 11):
        role = roles[(index - 1) % len(roles)]
        user, user_created = PilotUser.objects.get_or_create(
            email=f"pilot{index}@ekokintsugi.com",
            defaults={
                "username": f"pilot{index}",
                "first_name": "Pilot",
                "last_name": f"User {index}",
                "phone": f"98765000{index:02d}",
                "role": role,
                "city": cities[(index - 1) % len(cities)],
                "address": f"{index} Circular Lane, Green District",
                "shoe_size": str(5 + (index % 5)),
                "start_date": f"2026-05-{index:02d}" if role == "intern" else None,
                "end_date": f"2026-07-{index:02d}" if role == "intern" else None,
                "is_demo_user": True,
            },
        )
        if user_created:
            user.password = make_password("pilot123")
            user.save(update_fields=["password"])
        elif not user.is_demo_user:
            user.is_demo_user = True
            user.save(update_fields=["is_demo_user"])

        Shoe.objects.get_or_create(
            user=user,
            defaults={
                "shoe_id": f"SHOE-{1000 + index}",
                "product_line": "Urban Scrap Runner" if index % 2 == 0 else "Kintsugi Street Sole",
                "size": user.shoe_size,
                "status": "Delivered" if index <= 4 else "Pre-booked",
            },
        )
        SymbolicTree.objects.get_or_create(
            user=user,
            defaults={
                "tree_id": f"TREE-{200 + index}",
                "plant_type": plant_types[(index - 1) % len(plant_types)],
                "location": f"Community Plot {index}, Eco Campus",
            },
        )
        account, _ = PointsAccount.objects.get_or_create(
            user=user,
            defaults={
                "total_earned": 100 + index * 10,
                "approved": 80 + index * 5,
                "used": 30 if index % 3 == 0 else 10,
            },
        )
        PointTransaction.objects.get_or_create(
            account=account,
            action_type="credit",
            amount=100 + index * 10,
            defaults={"note": "Pilot onboarding bonus"},
        )

    user1 = PilotUser.objects.get(email="pilot1@ekokintsugi.com")
    user2 = PilotUser.objects.get(email="pilot2@ekokintsugi.com")
    user3 = PilotUser.objects.get(email="pilot3@ekokintsugi.com")

    WeeklyReview.objects.get_or_create(
        user=user1,
        week=1,
        defaults={
            "days_worn": 5,
            "hours_per_day": 6,
            "comfort": 4,
            "fit": 5,
            "sole": 4,
            "material": 4,
            "stitching": 5,
            "feedback": "Comfortable on daily commute, slight warmth after long walks.",
        },
    )
    WeeklyReview.objects.get_or_create(
        user=user2,
        week=1,
        defaults={
            "days_worn": 4,
            "hours_per_day": 5,
            "comfort": 4,
            "fit": 4,
            "sole": 4,
            "material": 5,
            "stitching": 4,
            "feedback": "Good grip and fit, material feels strong.",
        },
    )
    ReturnRequest.objects.get_or_create(
        user=user3,
        defaults={
            "shoe": user3.shoe,
            "reason": "Pilot period completed",
            "condition": "Good",
            "status": "Requested",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("pilot", "0002_pilotuser_is_demo_user"),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, migrations.RunPython.noop),
    ]
