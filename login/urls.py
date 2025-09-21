from django.urls import path
from . import views

app_name = "user_login"

urlpatterns = [
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register_view, name="register"),
    path("magic/", views.magic_link_request, name="magic"),
    path("verify/<str:token>/", views.verify_token, name="verify_token"),
]