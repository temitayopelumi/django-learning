from django.shortcuts import render, redirect
from .models import *
from .forms  import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
# Create your views here.
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'check/home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request, 'check/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer=Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'check/customer.html', context)

@login_required(login_url='login')
@admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers=Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders,
                'delivered':delivered, 'pending': pending}
    return render(request, 'check/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='Pending').count()
    context ={'orders':orders,'total_orders':total_orders,'delivered':delivered, 'pending': pending}
    return render(request, 'check/user.html', context)



@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username =  form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
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
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'check/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
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