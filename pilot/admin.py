from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PilotUser, PointsAccount, PointTransaction, ReturnRequest, Shoe, SymbolicTree, WeeklyReview


@admin.register(PilotUser)
class PilotUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Pilot profile",
            {
                "fields": (
                    "phone",
                    "role",
                    "city",
                    "address",
                    "shoe_size",
                    "start_date",
                    "end_date",
                    "qr_token",
                )
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "role", "is_staff")
    ordering = ("email",)


admin.site.register(Shoe)
admin.site.register(SymbolicTree)
admin.site.register(PointsAccount)
admin.site.register(PointTransaction)
admin.site.register(WeeklyReview)
admin.site.register(ReturnRequest)
