from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from core.models import *
from core.models import Category

# Create your views here.
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    return render(request, 'admin/admin_dashboard.html')

def user_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    total_user=User.objects.count()
    active=User.objects.filter(is_active=True).count()
    users=User.objects.all()
    return render(request,'admin/admin_user.html',{"count":total_user,"active":active,"user":users})



def admin_category(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    categories = Category.objects.prefetch_related('subcategory_set').all()
    return render(request, 'admin/admin_category.html', {'categories': categories})

def add_category(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category = Category()
        category.category_name = request.POST.get("category_name")
        category.category_description = request.POST.get("category_description")
        image = request.FILES.get('category_image')
        if image:
            category.category_image = image
        category.created_at = request.POST.get("created_at")
        category.slug = request.POST.get("slug")
        category.is_active = '_save' in request.POST or '_addanother' in request.POST or '_continue' in request.POST
        category.save()
        
        parent_id = request.POST.get('category')
        if parent_id:
            from core.models import SubCategory
            subcategory = SubCategory()
            subcategory.category_id = int(parent_id)
            subcategory.subcategory_name = category.category_name
            subcategory.subcategory_description = category.category_description
            subcategory.subcategory_image = category.category_image
            subcategory.created_at = category.created_at
            subcategory.slug = category.slug
            subcategory.is_active = True
            subcategory.save()
            messages.success(request, f'Subcategory "{category.category_name}" added under parent category!')
        else:
            messages.success(request, 'Category added successfully!')
        
        if '_addanother' in request.POST:
            messages.info(request, 'Ready to add another!')
            return render(request, 'admin/add_category.html', {'categories': categories})
        elif '_continue' in request.POST:
            messages.info(request, 'Continue editing form.')
            return render(request, 'admin/add_category.html', {'categories': categories})
        else:
            return redirect('admin_category')
    
    return render(request, 'admin/add_category.html', {'categories': categories})

def delete_category(request,id):
    categroy=Category.objects.get(id=id)
    categroy.delete()
    return redirect('admin_category')

def add_user(request):
    if request.method=="POST":
        user=User()
        user.username=request.POST.get('username')
        user.password=request.POST.get('password')
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.email=request.POST.get('email')
        image = request.FILES.get('profiley_image')
        if image:
            user.profile_image = image
        user.role=request.POST.get('role')
        user.phone_number=request.POST.get('phone_number')
        dob = request.POST.get('dob')
        if dob:
            user.dob=dob
        user.save()
        return redirect('admin_user')
    return render(request,'admin/add_user.html')

def toggle_user_status(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'User {"blocked" if user.is_active == False else "unblocked"} successfully!')
        except User.DoesNotExist:
            messages.error(request, 'User not found!')
    
    return redirect('admin_user')

def edit_category(request, category_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You are not authorized as admin")
        return redirect('admin_login')
    
    category = Category.objects.get(id=category_id)
    
    if request.method == 'POST':
        category.category_name = request.POST.get('category_name')
        category.category_description = request.POST.get('category_description')
        if 'category_image' in request.FILES:
            category.category_image = request.FILES['category_image']
        category.slug = request.POST.get('slug')
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('admin_category')
    
    return render(request, 'admin/edit_category.html', {'category': category})
