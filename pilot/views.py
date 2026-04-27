from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    AdminCreateUserForm,
    EmailAuthenticationForm,
    PilotSignupForm,
    PointsAdjustmentForm,
    ReturnRequestForm,
    ReturnStatusForm,
    WeeklyReviewForm,
)
from .models import PilotUser, PointTransaction, PointsAccount, ReturnRequest, Shoe, SymbolicTree

MAX_LIVE_PILOT_USERS = 10


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_staff:
            return HttpResponseForbidden("Admin access only.")
        return view_func(request, *args, **kwargs)

    return wrapped


def create_username(email):
    base = email.split("@")[0].replace(".", "").replace("+", "")
    username = base
    counter = 1
    while PilotUser.objects.filter(username=username).exists():
        counter += 1
        username = f"{base}{counter}"
    return username


def create_pilot_bundle(user):
    count = PilotUser.objects.filter(is_staff=False).count()
    Shoe.objects.get_or_create(
        user=user,
        defaults={
            "shoe_id": f"SHOE-{1000 + count}",
            "product_line": "Pilot Circular Runner",
            "size": user.shoe_size or "8",
            "status": Shoe.STATUS_PREBOOKED,
        },
    )
    SymbolicTree.objects.get_or_create(
        user=user,
        defaults={
            "tree_id": f"TREE-{300 + count}",
            "plant_type": "Neem",
            "location": "Community Plot New",
            "status": "Symbolic Tree Parent",
        },
    )
    PointsAccount.objects.get_or_create(user=user)


def live_pilot_user_count():
    return PilotUser.objects.filter(is_staff=False, is_demo_user=False).count()


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin-dashboard")
        return redirect("dashboard")
    return redirect("login")


def login_view(request):
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        email = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password", "")
        user = PilotUser.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return redirect("admin-dashboard" if user.is_staff else "dashboard")
        messages.error(request, "Invalid email or password.")
    return render(request, "pilot/login.html", {"form": form})


def signup_view(request):
    form = PilotSignupForm(request.POST or None)
    if request.method == "POST":
        if live_pilot_user_count() >= MAX_LIVE_PILOT_USERS:
            messages.error(request, "Pilot is full. Only 10 live users are allowed.")
        elif form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = create_username(user.email)
            user.is_demo_user = False
            user.set_password(form.cleaned_data["password"])
            user.save()
            create_pilot_bundle(user)
            messages.success(request, "Pilot account created. Please log in.")
            return redirect("login")
    return render(
        request,
        "pilot/signup.html",
        {
            "form": form,
            "pilot_full": live_pilot_user_count() >= MAX_LIVE_PILOT_USERS,
            "live_user_count": live_pilot_user_count(),
            "max_live_users": MAX_LIVE_PILOT_USERS,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect("admin-dashboard")
    return render(
        request,
        "pilot/dashboard.html",
        {
            "pilot_user": request.user,
            "points": request.user.points_account,
            "reviews": request.user.reviews.all(),
            "review_progress": request.user.reviews.count(),
            "qr_url": request.build_absolute_uri(reverse("qr-dashboard", args=[request.user.qr_token])),
        },
    )


@login_required
def review_create_view(request):
    if request.user.is_staff:
        return redirect("admin-dashboard")
    form = WeeklyReviewForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        messages.success(request, "Weekly review submitted.")
        return redirect("dashboard")
    return render(request, "pilot/review_form.html", {"form": form})


@login_required
def return_request_view(request):
    if request.user.is_staff:
        return redirect("admin-dashboard")
    existing = getattr(request.user, "return_request", None)
    if existing:
        return render(request, "pilot/return_form.html", {"existing": existing, "form": None})
    form = ReturnRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        return_request = form.save(commit=False)
        return_request.user = request.user
        return_request.shoe = request.user.shoe
        return_request.save()
        request.user.shoe.status = Shoe.STATUS_RETURNED
        request.user.shoe.save(update_fields=["status"])
        messages.success(request, "Return request submitted.")
        return redirect("dashboard")
    return render(request, "pilot/return_form.html", {"form": form, "existing": None})


def qr_dashboard_view(request, token):
    pilot_user = get_object_or_404(PilotUser, qr_token=token)
    return render(
        request,
        "pilot/qr_dashboard.html",
        {
            "pilot_user": pilot_user,
            "points": getattr(pilot_user, "points_account", None),
            "reviews": pilot_user.reviews.all(),
        },
    )


@admin_required
def admin_dashboard_view(request):
    users = PilotUser.objects.filter(is_staff=False).select_related("shoe", "tree", "points_account")
    create_form = AdminCreateUserForm(request.POST or None, prefix="create")
    if request.method == "POST" and request.POST.get("form_name") == "create-user":
        if live_pilot_user_count() >= MAX_LIVE_PILOT_USERS:
            messages.error(request, "Pilot is full. Only 10 live users are allowed.")
        elif create_form.is_valid():
            user = create_form.save(commit=False)
            user.email = user.email.lower()
            user.username = create_username(user.email)
            user.is_demo_user = False
            user.set_password(create_form.cleaned_data["password"])
            user.save()
            create_pilot_bundle(user)
            messages.success(request, "Pilot user created.")
            return redirect("admin-dashboard")

    review_rows = []
    delivered_count = 0
    total_reviews = 0
    for user in users:
        completed_weeks = list(user.reviews.values_list("week", flat=True))
        review_rows.append(
            {
                "user": user,
                "completed_count": len(completed_weeks),
                "week_statuses": [
                    {"week": week, "done": week in completed_weeks} for week in range(1, 9)
                ],
            }
        )
        total_reviews += len(completed_weeks)
        if user.shoe.status == Shoe.STATUS_DELIVERED:
            delivered_count += 1

    return render(
        request,
        "pilot/admin_dashboard.html",
        {
            "users": users,
            "returns": ReturnRequest.objects.select_related("user", "shoe"),
            "create_form": create_form,
            "points_form": PointsAdjustmentForm(),
            "return_form_class": ReturnStatusForm,
            "review_rows": review_rows,
            "total_reviews": total_reviews,
            "delivered_count": delivered_count,
            "live_user_count": live_pilot_user_count(),
            "max_live_users": MAX_LIVE_PILOT_USERS,
        },
    )


@admin_required
def update_points_view(request, user_id):
    user = get_object_or_404(PilotUser, pk=user_id, is_staff=False)
    form = PointsAdjustmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account, _ = PointsAccount.objects.get_or_create(user=user)
        amount = form.cleaned_data["amount"]
        action_type = form.cleaned_data["action_type"]
        if action_type == "credit":
            account.total_earned += amount
        elif action_type == "approve":
            account.approved += amount
        elif action_type == "redeem":
            account.used += amount
        account.save()
        PointTransaction.objects.create(account=account, action_type=action_type, amount=amount, note="Admin action")
        messages.success(request, "Points updated.")
    return redirect("admin-dashboard")


@admin_required
def update_return_view(request, return_id):
    return_request = get_object_or_404(ReturnRequest, pk=return_id)
    form = ReturnStatusForm(request.POST or None, instance=return_request)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Return workflow updated.")
    return redirect("admin-dashboard")
