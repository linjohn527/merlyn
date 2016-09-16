# _*_ coding:utf-8 _*_
# __auth__: LJ

from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone

@login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    # 登录视图
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        print email, password
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.invalid_time:
                if user.invalid_time > timezone.now() and timezone.now() > user.valid_time: # 账号在有效期内
                    auth.login(request, user)
                    request.session.set_expiry(60*30)

                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {'login_err': 'Account expired, contact admin!'})
            elif user.valid_time < timezone.now():
                auth.login(request, user)
                request.session.set_expiry(60*30)
                return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'login_err': 'Username or Password incorrect!'})

    else:
        return render(request, 'login.html')


def logout(request):
    # 退出登录
    auth.logout(request)
    return render(request, 'login.html')