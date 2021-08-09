
from django.contrib import auth
from django.contrib.messages.api import success
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Book,Category,Videos
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):     
    return render(request,"home.html")

def logout(request):
    return render(request,"logout.html")
def register(request): 
    if request.method=="POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            messages.error(request,"invalid user")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"invalid email")
        else:
            if password1==password2:
                User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password1, username=username)    
                messages.success(request,"register successfully")
                return redirect("/")
            else:
                messages.error(request,"password not match")
    return render(request,"register.html")
def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        print(username)
        password1=request.POST.get("password1")
        print(password1)
        user=authenticate(username=username,password=password1)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        messages.success(request,"invalid user")

    return render(request,"login.html")
def logout(request):
    auth.logout(request)
    messages.success(request,"user succesfully logout")
    return redirect("/")

def about(request):
    video = Videos.objects.all()
    context = {
        'video' : video
    }
    return render(request,"about.html",context=context)



def upload_video(request):
     
    if request.method == 'POST': 
         
        title = request.POST['title']
        video = request.POST['video']
         
        content = Videos(title=title,video=video)
        content.save()
        return redirect('home')
     
    return render(request,'upload.html')
 
 
def display(request):
     
    videos = Videos.objects.all()
    context ={
        'videos':videos,
    }
     
    return render(request,'videos.html',context)
def book(request):
    category=Category.objects.all()
    book=None
    categoryid=request.GET.get('category')
    if categoryid:
        book=Book.book_by_category(category_id=categoryid)
    else:
        book=Book.objects.all()
    context={
        'category':category,
        'book':book
    }
    return render(request,'book.html',context=context)
import razorpay

client=razorpay.Client(auth=("rzp_test_CYaXIJ7TIInUip","g6BjPANgPF7P7DDQyyJp9knF"))
@login_required
def payment(request,book_id):
    if request.user.is_authenticated:
        user=request.user
    else:
        return redirect ("/login")
    book=Book.objects.get(id=book_id)
    print(book)
    order_amount = "50000"
    order_currency = "INR"
    order_receipt = "order_rcptid_11"

    DATA={
        'amount':order_amount,
        'currency':order_currency,
        'receipt':order_receipt
    }
    order=client.order.create(data=DATA)
    context={
        'book':book,
        'order':order
    }
    payment = Payment(user=user,book=book,orderid=order.get('id'),status="FAIL")
    payment.save()
    return render(request,'payment.html',context=context)
def verifypayment(request):
    if request.method=="POST":
        razorpay_payment_id=request.POST.get('razorpay_payment_id')
        razorpay_order_id=request.POST.GET('razorpay_order_id')
        razorpay_signature=request.POST.get('razorpay_signature')
        param_dict={
            'razorpay_payment_id':razorpay_payment_id,
            'razorpay_order_id':razorpay_order_id,        
            'razorpay_signature':razorpay_signature
            }
        client.utility.verify_payment_signature(param_dict)
        payment = Payment.objects.get(orderid=razorpay_order_id)
        payment.status = "SUCCESS"
        payment.paymentid = razorpay_payment_id
        payment.save()
        orders = Myorder(user=payment.user,book=payment.book)
        orders.save()
    return HttpResponse("payment successful")
def order(request):
    if request.user.is_authenticated:
        user=request.user
    orders=Myorder.objects.filter(user=user)
    context={
        'orders':orders
    }
    return render(request,'order.html',context=context)
def see(request,book_id):
    book=Book.objects.filter(id=book_id)
    context={
        'books':book
    }
    return render(request,"see.html",context=context)