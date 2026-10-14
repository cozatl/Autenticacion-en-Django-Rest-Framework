from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from rest_framework import permissions, viewsets

from .forms import LoginForm, RegisterForm
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, updated, or deleted.
    """

    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        # Redirects to the login page after successful registration
        return redirect("accounts:login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        # Redirects to the sales page after successful login
        return redirect("sales:sales")

    context = {"form": form}
    return render(request, "accounts/login.html", context)
