from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("review/", views.review_create_view, name="review"),
    path("return/", views.return_request_view, name="return-request"),
    path("pilot/<uuid:token>/", views.qr_dashboard_view, name="qr-dashboard"),
    path("admin-panel/", views.admin_dashboard_view, name="admin-dashboard"),
    path("admin-panel/points/<int:user_id>/", views.update_points_view, name="update-points"),
    path("admin-panel/returns/<int:return_id>/", views.update_return_view, name="update-return"),
]
