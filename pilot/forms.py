from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import PilotUser, ReturnRequest, WeeklyReview


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)


class PilotSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = PilotUser
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "role",
            "city",
            "address",
            "shoe_size",
            "start_date",
            "end_date",
            "password",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class WeeklyReviewForm(forms.ModelForm):
    class Meta:
        model = WeeklyReview
        fields = [
            "week",
            "days_worn",
            "hours_per_day",
            "comfort",
            "fit",
            "sole",
            "material",
            "stitching",
            "feedback",
            "image",
        ]
        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        used_weeks = set()
        if user:
          used_weeks = set(user.reviews.values_list("week", flat=True))
        self.fields["week"].widget = forms.Select(
            choices=[(week, f"Week {week}") for week in range(1, 9) if week not in used_weeks]
        )

    def clean(self):
        cleaned = super().clean()
        week = cleaned.get("week")
        if self.user and week and self.user.reviews.filter(week=week).exists():
            raise forms.ValidationError("A review for this week already exists.")
        if self.user and self.user.reviews.count() >= 8:
            raise forms.ValidationError("Maximum 8 reviews allowed.")
        return cleaned


class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ["reason", "condition"]
        widgets = {
            "reason": forms.Textarea(attrs={"rows": 4}),
        }


class PointsAdjustmentForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    action_type = forms.ChoiceField(
        choices=[
            ("credit", "Add points"),
            ("approve", "Approve points"),
            ("redeem", "Redeem points"),
        ]
    )


class ReturnStatusForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ["status", "final_action"]


class AdminCreateUserForm(PilotSignupForm):
    class Meta(PilotSignupForm.Meta):
        fields = PilotSignupForm.Meta.fields
