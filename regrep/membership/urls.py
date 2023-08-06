from django.urls import path, include

from regrep.membership.views import register, login_view, logout_view, index

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("/", index, name="index"),
]