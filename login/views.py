import uuid
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from .models import MagicLinkToken
from .forms import RegisterForm, LoginForm, MagicLinkForm

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("/")  # редирект после логина
    else:
        form = LoginForm()
    return render(request, "login/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = uuid.uuid4().hex
            MagicLinkToken.objects.create(email=user.email, token=token)
            link = request.build_absolute_uri(f"/accounts/verify/{token}/")
            # Для разработки — печать в консоль. В проде — отправлять email.
            print("Magic link:", link)
            messages.success(request, "Готово — ссылка подтверждения в консоли.")
            return redirect("login:login_view")
    else:
        form = RegisterForm()
    return render(request, "login/register.html", {"form": form})


def magic_link_request(request):
    if request.method == "POST":
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            token = uuid.uuid4().hex
            MagicLinkToken.objects.create(email=email, token=token)
            link = request.build_absolute_uri(f"/accounts/verify/{token}/")
            print("Magic link:", link)
            messages.success(request, "Ссылка отправлена (выведена в консоль).")
            return redirect("login:login_view")
    else:
        form = MagicLinkForm()
    return render(request, "login/magic_link.html", {"form": form})


def verify_token(request, token):
    token_obj = get_object_or_404(MagicLinkToken, token=token)

    if timezone.now() - token_obj.create_at > timedelta(minutes=15):
        token_obj.delete()
        return render(request, "login/verify_failed.html", {"reason": "expired"})

    try:
        user = User.objects.get(email__iexact=token_obj.email)
    except User.DoesNotExist:
        token_obj.delete()
        return render(request, "login/verify_failed.html", {"reason": "no_user"})

    user.is_active = True
    user.save()
    auth_login(request, user)
    token_obj.delete()
    return redirect("/")
