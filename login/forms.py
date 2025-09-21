from typing import Optional
from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UsernameField

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "class": "input"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Повторите пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль", "class": "input"}),
    )

    class Meta:
        model = User
        fields = ("email", "username")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email", "class": "input"}),
            "username": forms.TextInput(attrs={"placeholder": "Имя (необязательно)", "class": "input"}),
        }

    def clean_email(self) -> str:
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError(_("Введите email"))
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Пользователь с таким email уже существует"))
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if not p1 or not p2:
            raise ValidationError(_("Введите пароль и подтверждение"))
        if p1 != p2:
            raise ValidationError(_("Пароли не совпадают"))
        password_validation.validate_password(p1, self.instance)
        return p2

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False 
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(
        label=_("Email или логин"),
        widget=forms.TextInput(attrs={"placeholder": "Email или логин", "class": "input"})
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "class": "input"})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user: Optional[User] = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        ident = (cleaned.get("identifier") or "").strip()
        pwd = cleaned.get("password")
        if not ident or not pwd:
            raise ValidationError(_("Укажите логин (или email) и пароль"))

        user = authenticate(self.request, username=ident, password=pwd)
        if user is None:
            try:
                u = User.objects.get(email__iexact=ident)
                user = authenticate(self.request, username=u.get_username(), password=pwd)
            except User.DoesNotExist:
                user = None

        if user is None:
            raise ValidationError(_("Неверный логин или пароль"))
        if not user.is_active:
            raise ValidationError(_("Аккаунт не активен"))
        self.user = user
        return cleaned

    def get_user(self) -> Optional[User]:
        return self.user


class MagicLinkForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"placeholder": "Email для ссылки", "class": "input"})
    )

    def clean_email(self) -> str:
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Пользователь с таким email не найден"))
        return email
