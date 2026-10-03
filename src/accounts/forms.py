from typing import ClassVar

from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ("email", "full_name")
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("The passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Email or password is incorrect.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return getattr(self, "user_cache", None)
