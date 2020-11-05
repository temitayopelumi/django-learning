from django.shortcuts import render, redirect
from .models import *
from .forms  import OrderForm
from django.forms import inlineformset_factory
# Create your views here.

def home(request):
    return render(request, 'check/home.html')

def products(request):
    products=Product.objects.all()
    return render(request, 'check/products.html',{'products':products})

def customer(request, pk):
    customer=User.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'check/customer.html', context)

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

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(User, Order, fields=('product', 'status'))
    customer = User.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objectst.none(), instance=customer)
    #form =  OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Print Post:', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,  'check/order_form.html', context)

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

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return  render(request, 'check/delete.html', context)