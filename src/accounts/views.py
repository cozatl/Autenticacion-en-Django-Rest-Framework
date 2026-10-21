from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from rest_framework import generics, permissions, viewsets

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
        return redirect("accounts:profile_page")

    context = {"form": form}
    return render(request, "accounts/login.html", context)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    A view that allows an authenticated user to view and update
    their own profile.
    """

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # Returns only the user who is logged in, validated via the JWT token.
        return self.request.user


@login_required
@never_cache
def profile_view(request):
    """
    HTML view to show user profile when their are
    logged in.
    """
    user = request.user
    return render(request, "accounts/profile.html", {"user": user})
