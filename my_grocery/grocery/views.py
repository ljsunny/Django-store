from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from django.views.generic import edit
from django import forms
from .models import *
from .forms import *
## for user authentication
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout

from .util.JsonUtil import JsonUtil
import os,json

def is_staff(user):
    return user.is_staff
# Create your views here.
navItems = [
    # {"link":"/grocery/","label":"Home"},
    # {"link":"/grocery/product-list","label":"Grocery"},
    # {"link":"/grocery/users/","label":"List of Users"},
    # {"link":"/grocery/product-history/","label":"product history"},
    # {"link":"/accounts/register","label":"Register"},
    # {"link":"/accounts/login","label":"Login"},
    # {"link":"/accounts/logout","label":"Logout","class":"d-none"},
    ]

def Index(request):
    num_product = Product.objects.all().count()
    content = {
        'num_product':num_product,
        'navItems':navItems,
    }
    content={
        'navItems':navItems,
    }
    return render(request,'index.html',context=content)

class ProductList(generic.ListView):
    model = Product
    queryset = Product.objects.all()
    context_object_name = "product_list"
    template_name = "product/list.html"

    def get_context_data(self, **kwargs: Any):
        context =  super(ProductList,self).get_context_data(**kwargs)
        context['navItems'] = navItems
        return context

## save item in the cart
def saveCart(request):
    product_name = request.POST.get("name")
    product_items = Product.objects.filter(name=product_name).values()[0] #select * from Product where name='dfg'
    product_new = {'product_id':product_items['id'], 'product_name':product_name,'price' : float(product_items['price']), 'amount':1}

    selectProduct(product_new,request.user.id)

    return redirect('product-list')

def cartDirbyUser(uid):
    return f"./grocery/data/{uid}/cart.json"

def selectProduct(CartInfo, uid): 
    # Create user directory path
    dir = os.path.dirname(cartDirbyUser(uid))
    isExistFile = os.path.exists(dir) 
    if not isExistFile:
        os.makedirs(dir)

    # Cart file path
    cart_file_path = cartDirbyUser(uid)

    # Initialize the basic structure if the cart is empty
    if not os.path.exists(cart_file_path):
        cart_data = {"cart": []}  # Initialized cart structure
    else:
        # Read cart from JSON file
        cart_data = JsonUtil.readFile(cart_file_path)

    # Search for the product in the cart
    for item in cart_data["cart"]:
        if item["product_name"] == CartInfo['product_name']:
            item["amount"] += 1  # Increase quantity
            break
    else:
        # Add new product (executed when the for loop ends normally)
        cart_data["cart"].append({
            "product_name": CartInfo['product_name'],
            "price": CartInfo['price'],
            "amount": 1
        })
    
    # Write updated cart to JSON file
    JsonUtil.writeFile(cart_file_path, cart_data)


##show cart
def showCart(request):
    if os.path.exists(cartDirbyUser(request.user.id)):
        cartList = JsonUtil.readFile(cartDirbyUser(request.user.id))['cart']
    else:
        cartList = []

    total_price=0
    for cart in cartList:
        total_price += cart['price'] * cart['amount']

    context = {
        'navItems':navItems,
        'cartList':cartList,
        'total_price':total_price,
        'cnt':len(cartList)
    }
    return render(request,'cart/list.html',context)

##doOrder
@login_required
def addOrder(request):
    total_price = request.POST.get("total_price")

    ## bring data from json file
    if os.path.exists(cartDirbyUser(request.user.id)):
        cartList = JsonUtil.readFile(cartDirbyUser(request.user.id))['cart']
        ##insert data into order history, order product
        order_history = OrderHistory(total_price= total_price, user_id = request.user.id)
        order_history.save()

        for cart in cartList:
            product = Product.objects.filter(name = cart['product_name'])
            order_product = OrderProduct(oid = order_history, product = product[0], amount = cart['amount'])

            order_product.save()

        ## delete json file 
        os.remove(cartDirbyUser(request.user.id))
        cartList=[]
        msg = {"code":"success","lbl":"Successfully added"}
    else:
        msg = {"code":"fail","lbl":"Cart is empty"}
    context = {
        "msg":msg,
        'navItems':navItems,
        'cartList':cartList,
        'cnt':len(cartList)
    }
    return render(request,'cart/list.html',context)

@user_passes_test(is_staff)
def ProductAdd(request):
    form = ProductForm()
    msg = False
    url = 'product/add-product.html'
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']

            product_items = Product.objects.filter(name=name).values() #select * from Genre where name='dfg'
            if len(product_items) == 0:
                product_new = Product(name=name, price=price, image=image) #Insert into Genre (name) values (dsgfg)
                product_new.save()
                msg = {"code":"success","lbl":"Record Added!"}
                return redirect('product-list')
            else:
                msg = {"code":"danger","lbl":"Record already exists!"}
    context = {
        'form':form,
        'navItems':navItems,
        'msg':msg
    }
    return render(request,url,context)

class ProductUpdate(UserPassesTestMixin,edit.UpdateView):
    login_required=True
    model = Product
    form_class = ProductForm 
    template_name = "product/update-product.html"
    success_url = "/grocery/product-list/"
    ## check staff
    def test_func(self):
        return self.request.user.is_staff  # True이면 접근 가능
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super(ProductUpdate,self).get_context_data(**kwargs)
        context['navItems'] = navItems
        return context

class OrderHistoryList(generic.ListView):
    model = OrderHistory
    context_object_name = "order_history"
    template_name = "order/list.html"

    def get_context_data(self, **kwargs: Any):
        context =  super(OrderHistoryList,self).get_context_data(**kwargs)
        context['navItems'] = navItems
        context['order_history'] = OrderHistory.objects.filter(user_id=self.kwargs['uid'])
        if(len(self.kwargs)>1):
            context['selectedOrder'] = OrderProduct.objects.filter(oid=self.kwargs['pk'])
        return context

@user_passes_test(is_staff)
def acceptStatus(request,pk):
    req = get_object_or_404(OrderHistory, id=pk)
    req.status = 'Approved'
    req.save()
    return redirect('transaction-list')

@user_passes_test(is_staff)
def denyStatus(request,pk):
    req = get_object_or_404(OrderHistory, id=pk)
    req.status = 'Deny'
    req.save()
    return redirect('transaction-list')

class TransactionList(UserPassesTestMixin,generic.ListView):
    model = OrderHistory
    queryset = OrderHistory.objects.all()

    context_object_name = "order_history"
    template_name = "transaction/list.html"
    def test_func(self):
        return self.request.user.is_staff  # True이면 접근 가능
    def get_context_data(self, **kwargs: Any):
        context =  super(TransactionList,self).get_context_data(**kwargs)
        context['navItems'] = navItems
        if(self.kwargs):
            context['selectedOrder'] = OrderProduct.objects.filter(oid=self.kwargs['pk'])
        return context

def RegisterView(request):
    form = RegisterForm()
    msg = False
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            newUser = User.objects.create_user(username=form.cleaned_data['uname'],
                                            password=form.cleaned_data['password'],
                                            email = form.cleaned_data['email']
                                            )
            newUser.first_name = form.cleaned_data['fname']
            newUser.last_name = form.cleaned_data['lname']
            newUser.save()
            msg = {"code":"success","lbl":"User Registed!"}
    context = {
        'form':form,
        'navItems':navItems,
        'msg':msg
    }
    return render(request,'register.html',context)

def changePasswordView(request):
    form = ChangePassForm()
    msg = False
    
    url = 'change_password.html'
    if request.method == "POST":
        form = ChangePassForm(request.POST)

        ##email is valid
        if form.is_valid():
            ## User is not exist
            if not User.objects.filter(email = form.data['email']) :
                msg = {"code":"danger","lbl":"User Not Exist"}
                context={
                    'form':form,
                    'navItems':navItems,
                    'msg':msg
                }
                return render(request,url,context)
            
            user = User.objects.get(email=form.data['email'])

                
            #old Password is not correct
            if not user.check_password(form.data['old_password']):
                msg = {"code":"danger","lbl":"Password is not correct"}
                context={
                    'form':form,
                    'navItems':navItems,
                    'msg':msg
                }
                return render(request,url,context)
            
            ##compare new_password and confirm_password
            if(form.data['new_password'] != form.data['confirm_password']):
                msg = {"code":"danger","lbl":"confirm password is not same to new password"}
                context={
                    'form':form,
                    'navItems':navItems,
                    'msg':msg
                }
                return render(request,url,context)
            
            #update user
            user.set_password(form.data['new_password'])
            user.save()
            msg = {"code":"success","lbl":"Password Changed!"}
    context = {
        'form':form,
        'navItems':navItems,
        'msg':msg
    }
    return render(request,url,context)


def LoginView(request):
    form = LoginForm()
    msg = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['uname'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                response = redirect("/")
                return response
            else:
                msg ={"code":"danger","lbl":"Failed Authentication!"}
    context = {
        'form':form,
        'navItems':navItems,
        'msg':msg
    }
    return render(request,'login.html',context)

def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("/accounts/login")