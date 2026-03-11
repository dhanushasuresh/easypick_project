from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from seller.models import ProductVariant

def main_home_view(request):
    return render(request,'core/main_home.html')
def login_view(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,password=password,username=email)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successfully')
            return redirect('home')
        else:
            messages.error(request,"invalid email  or password")
            return redirect('login')
    return render(request,'core/login.html')
def shop_view(request):
    product=ProductVariant.objects.all().select_related('product').prefetch_related('images')
    return render(request,'core/shop.html',{'product':product})
def logout_view(request):
    logout(request)
    messages.success(request,"Logout")
    return redirect("login")
