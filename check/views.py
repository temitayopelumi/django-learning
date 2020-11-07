from django.shortcuts import render, redirect
from .models import *
from .forms  import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    return render(request, 'check/home.html')
    
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username =  form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            messages.success(request, 'Account was created for'+username)
            return redirect('login')
    
    context = {'form':form}
    return render(request, "check/register.html", context)

    
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'User or Password is incorrect')
    context = {}
    return render(request, "check/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request, 'check/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer=User.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter': myFilter}
    return render(request, 'check/customer.html', context)

@login_required(login_url='login')
@admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers=User.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='Pending').count()


    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders,
                'delivered':delivered, 'pending': pending}
    return render(request, 'check/dashboard.html', context)

def userPage(request):
    context ={}
    return render(request, 'check/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(User, Order, fields=('product', 'status'))
    customer = User.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form =  OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Print Post:', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,  'check/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form  =OrderForm(instance=order)
    if request.method == 'POST':
        #print('Print Post:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={'form':form}
    return render(request, 'check/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return  render(request, 'check/delete.html', context)