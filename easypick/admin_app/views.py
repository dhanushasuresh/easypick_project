from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from core.models import *

# Create your views here.
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    return render(request, 'admin/admin_dashboard.html')

def user_view(request):
    total_user=User.objects.count()
    active=User.objects.filter(is_active=True).count()
    users=User.objects.all()
    return render(request,'admin/admin_user.html',{"count":total_user,"active":active,"user":users})
