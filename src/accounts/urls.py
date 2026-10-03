from django.urls import path

from accounts.views import login_view, register_view

# Define namespace which is required for the template
app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
]
