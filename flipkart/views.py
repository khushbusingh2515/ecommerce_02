from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from .models import *

from django.contrib.auth.hashers import check_password,make_password

def index(request):

    if request.method == 'POST':
        product_id = request.POST.get('productid')
        remove = request.POST.get('remove')
        print('Product_id----------->', product_id)

        cart_id = request.session.get('cart')
        print('cart_id----------->', cart_id)
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                       cart_id.pop(product_id)
                    else:
                       cart_id[product_id] = quantity -1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] =  1
        request.session['cart'] = cart_id
        print('request.session[cart]----------->', request.session['cart'])

    category_obj = Category.objects.all()
    category_id = request.GET.get("category_id")
    search = request.GET.get("search")

    if category_id:
        product_obj = Product.objects.filter(product_category=category_id)
    elif search:
        product_obj = Product.objects.filter(product_name__icontains=search)
    else:
        product_obj = Product.objects.all()

    context = {
        "category": category_obj,
        "product": product_obj,
    }

    return render(request, 'home.html',context=context)



def sign_up(request):
    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mbl')
        gender = request.POST.get('gender')

        reg_obj = Registration(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender
        )

        reg_obj.save()

        return redirect('home')
    


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_id = Registration.objects.get(email=email)
        try:
            if check_password(password,email_id.password):
                request.session['name'] = email_id.first_name
                return redirect('home')
            else:
                return HttpResponse("wrong password")
        except:
            return HttpResponse("wrong email")
        

def logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):
    
    cart_id = list(request.session.get('cart').keys())

    product = Product.objects.filter(id__in = cart_id)

    context = {
        'product': product
    }

    return render(request,'cart.html',context=context)