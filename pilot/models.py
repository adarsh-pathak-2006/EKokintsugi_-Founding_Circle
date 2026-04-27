import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PilotUser(AbstractUser):
    ROLE_INTERN = "intern"
    ROLE_TEAM = "team"
    ROLE_SUPPORTER = "supporter"
    ROLE_CHOICES = [
      (ROLE_INTERN, "Intern"),
      (ROLE_TEAM, "Team"),
      (ROLE_SUPPORTER, "Supporter"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_SUPPORTER)
    city = models.CharField(max_length=120, blank=True)
    address = models.TextField(blank=True)
    shoe_size = models.CharField(max_length=10, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def clean(self):
        super().clean()
        if self.role == self.ROLE_INTERN and (not self.start_date or not self.end_date):
            raise ValidationError("Interns must have start and end dates.")

    def __str__(self):
        return self.get_full_name() or self.email


class Shoe(models.Model):
    STATUS_PREBOOKED = "Pre-booked"
    STATUS_DELIVERED = "Delivered"
    STATUS_RETURNED = "Returned"
    STATUS_CHOICES = [
        (STATUS_PREBOOKED, "Pre-booked"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_RETURNED, "Returned"),
    ]

    user = models.OneToOneField(PilotUser, on_delete=models.CASCADE, related_name="shoe")
    shoe_id = models.CharField(max_length=40, unique=True)
    product_line = models.CharField(max_length=120)
    size = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PREBOOKED)

    def __str__(self):
        return self.shoe_id


class SymbolicTree(models.Model):
    user = models.OneToOneField(PilotUser, on_delete=models.CASCADE, related_name="tree")
    tree_id = models.CharField(max_length=40, unique=True)
    plant_type = models.CharField(max_length=80)
    location = models.CharField(max_length=140)
    status = models.CharField(max_length=80, default="Symbolic Tree Parent")

    def __str__(self):
        return self.tree_id


class PointsAccount(models.Model):
    user = models.OneToOneField(PilotUser, on_delete=models.CASCADE, related_name="points_account")
    total_earned = models.PositiveIntegerField(default=0)
    approved = models.PositiveIntegerField(default=0)
    used = models.PositiveIntegerField(default=0)

    @property
    def remaining(self):
        return self.approved - self.used

    def __str__(self):
        return f"Points for {self.user}"


class PointTransaction(models.Model):
    TYPE_CREDIT = "credit"
    TYPE_APPROVE = "approve"
    TYPE_REDEEM = "redeem"
    TYPE_CHOICES = [
        (TYPE_CREDIT, "Credit"),
        (TYPE_APPROVE, "Approve"),
        (TYPE_REDEEM, "Redeem"),
    ]

    account = models.ForeignKey(PointsAccount, on_delete=models.CASCADE, related_name="transactions")
    action_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.PositiveIntegerField()
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action_type} {self.amount} for {self.account.user}"


class WeeklyReview(models.Model):
    user = models.ForeignKey(PilotUser, on_delete=models.CASCADE, related_name="reviews")
    week = models.PositiveSmallIntegerField()
    days_worn = models.PositiveSmallIntegerField()
    hours_per_day = models.PositiveSmallIntegerField()
    comfort = models.PositiveSmallIntegerField()
    fit = models.PositiveSmallIntegerField()
    sole = models.PositiveSmallIntegerField()
    material = models.PositiveSmallIntegerField()
    stitching = models.PositiveSmallIntegerField()
    feedback = models.TextField()
    image = models.FileField(upload_to="reviews/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["week", "created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "week"], name="unique_review_per_user_week"),
        ]

    def clean(self):
        super().clean()
        if not 1 <= self.week <= 8:
            raise ValidationError("Week must be between 1 and 8.")

    def __str__(self):
        return f"{self.user} week {self.week}"


class ReturnRequest(models.Model):
    STATUS_REQUESTED = "Requested"
    STATUS_RECEIVED = "Received"
    STATUS_COMPLETED = "Completed"
    STATUS_CHOICES = [
        (STATUS_REQUESTED, "Requested"),
        (STATUS_RECEIVED, "Received"),
        (STATUS_COMPLETED, "Completed"),
    ]

    ACTION_REPAIR = "Repair"
    ACTION_REUSE = "Reuse"
    ACTION_RECYCLE = "Recycle"
    FINAL_ACTION_CHOICES = [
        (ACTION_REPAIR, "Repair"),
        (ACTION_REUSE, "Reuse"),
        (ACTION_RECYCLE, "Recycle"),
    ]

    CONDITION_GOOD = "Good"
    CONDITION_FAIR = "Fair"
    CONDITION_DAMAGED = "Damaged"
    CONDITION_CHOICES = [
        (CONDITION_GOOD, "Good"),
        (CONDITION_FAIR, "Fair"),
        (CONDITION_DAMAGED, "Damaged"),
    ]

    user = models.OneToOneField(PilotUser, on_delete=models.CASCADE, related_name="return_request")
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name="return_requests")
    reason = models.TextField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REQUESTED)
    final_action = models.CharField(max_length=20, choices=FINAL_ACTION_CHOICES, blank=True)
    requested_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return for {self.user}"
