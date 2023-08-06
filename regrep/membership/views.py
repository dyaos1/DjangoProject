from django.shortcuts import render, redirect, HttpResponse

from regrep.membership.forms import RegisterUserForm, RegisterMemberForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

# Create your views here.


@login_required
def index(req):
    if req.user.is_authenticated:
        username = req.user.username
    else:
        username = "불청객"
    
    return render(req, 'index.html', {"username": username})


def register(req):
    msg = ""

    if req.method == "POST":
        userform = RegisterUserForm(req.POST)
        memberform = RegisterMemberForm(req.POST)

        if userform.is_valid() and memberform.is_valid():
            member = memberform.save(commit=False)
            member.user = userform.save()
            member.save()

            username = userform.cleaned_data.get("username")
            raw_pwd = userform.cleaned_data.get("password1")

            user = authenticate(username=username, password=raw_pwd)
            login(req, user)
            msg = "회원가입완료"

        else:
            msg = "잘못된 요청입니다."

    else:
        userform = RegisterUserForm()
        memberform = RegisterMemberForm()

    return render(req, "auth/register.html", {"userform": userform, "memberform":memberform, "msg": msg})


def login_view(req):
    msg = ""
    if req.method == "POST":
        form = AuthenticationForm(req, req.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )

            if user is not None:
                login(req, user)
                msg = "로그인 성공"
            return redirect("index")

        msg = "로그인 실패"

    else:
        form = AuthenticationForm()

    return render(req, "auth/login.html", {"form": form, "msg": msg})


def logout_view(req):
    logout(req)
    return redirect("login")