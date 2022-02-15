from django.urls import path

from accounts.views import LoginUserView, LogoutUserView, SignupStaffUserView

urlpatterns = [
    path("staff-signup/", SignupStaffUserView.as_view(), name="staff_signup"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
]
