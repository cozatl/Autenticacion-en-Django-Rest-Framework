from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import (
    UserProfileView,
    login_view,
    profile_view,
    register_view,
)

# Define namespace which is required for the template
app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("profile/", profile_view, name="profile_page"),
    path(
        "logout/",
        LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path("api/v1/profile/", UserProfileView.as_view(), name="user-profile"),
    path("api/v1/token/", TokenObtainPairView.as_view()),
    path("api/v1/token/refresh/", TokenRefreshView.as_view()),
]
