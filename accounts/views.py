from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm
# Create your views here.
from .models import *


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user)
            messages.success(request, 'Account was created for %s' % form.cleaned_data.get('username'))
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'username or password is incorrct')
            # return render(request, 'accounts/login.html')

    context = {}
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def dashboard(request):

    accounts = Account.objects.all()
    total_accounts = accounts.count()

    # return HttpResponse(delivered)
    context = {

        'accounts': accounts,
        'total_orders': [],
        'total_accounts': total_accounts,
        'delivered': [],
        'pending': []
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['account'])
def userPage(request):
    orders = request.user.account.order_set.all()
    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    delivered = orders.filter(status='Delivered').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def account(request, id):
    account = Account.objects.get(id=id)
    orders = account.order_set.all()
    order_count = orders.count()

    context = {
        'account': account,
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'accounts/account.html', context)
