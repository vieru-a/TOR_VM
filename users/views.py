from django.shortcuts import render
from .forms import LoginUserForm


def login_user(requests):
    form = LoginUserForm()
    return render(requests, 'users/login.html', {'form': form})


def logout_user(requests):
    pass
