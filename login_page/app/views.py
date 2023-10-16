from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from . models import CustomUser
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserEditForm
from django.db.models import Q

# Create your views here.


@never_cache
def login_page(request):
      
    if 'username' in request.session:
        return redirect('home_page')
    if 'is_superuser' in request.session:
        return redirect('admin_dashboard_page')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            
            if user.is_superuser:
                request.session['is_superuser'] = username
                return redirect('admin_dashboard_page')
            else:
                request.session['username'] = username
                return redirect('home_page')

        else:
            try:
                user = CustomUser.objects.get(username=username)
                messages.error(request, 'Incorrect password', extra_tags='invalid-login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist', extra_tags='invalid-login')
    return render (request, "login.html") 


@never_cache
def signup_page(request):
    if 'username' in request.session:
        return redirect(home_page)
    if 'is_superuser' in request.session:
        return redirect(admin_dashboard_page)
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if CustomUser.objects.filter(username=uname).exists():
            messages.warning(request, 'Username already exists')

        elif CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')

        elif pass1 != pass2:
            messages.warning(request, "Passwords doesn't match")

        else:
            my_user = CustomUser.objects.create_user(username = uname, email = email, password = pass1)
            my_user.save()
            return redirect('login_page')
        
    return render (request, 'signup.html')


@never_cache
def home_page(request):
    if 'username' in request.session:
        return render (request, 'home.html')
    if 'is_superuser' in request.session:
        return render (request, 'home.html')
    
    return redirect ('login_page')


@never_cache
def admin_dashboard_page(request):
    form = UserEditForm()
    users = CustomUser.objects.all().order_by('id')  
    if 'is_superuser' in request.session:
        return render(request, 'dashboard.html', {'form': form, 'user': users})
    
    return redirect ('login_page')
    


# Save data in admin page
@never_cache
def save_data(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        usr_id = request.POST.get('userid')

        if CustomUser.objects.filter(username=username):
            cur_usr = CustomUser.objects.get(username=username)
            us_id = cur_usr.id
        else:            
            us_id = id
                
        if CustomUser.objects.filter(username=username and us_id !=usr_id).exists():
            messages.warning(request, 'Username already exists')
        elif CustomUser.objects.filter(email=email and us_id !=usr_id).exists():
            messages.warning(request, 'Email already exists')
        else:
            user_id = request.POST.get('userid')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
            else:
                if CustomUser.objects.filter(username = username).exists():
                    messages.warning(request, "username already exist!")
                elif CustomUser.objects.filter(email = email).exists():
                    messages.warning(request, "email alrady exists!")
                else:
                    my_user = CustomUser.objects.create_user(username=username, email=email, password=password)

                    my_user.save()
            return redirect('admin_dashboard_page')
    return redirect('admin_dashboard_page')

        
# Delete data
@never_cache
def delete_data(request,user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'status': 'Success', 'message': 'User deleted successfully'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'status': 'Error', 'message': 'User not found'})
    

    
# Search data
@never_cache
def search_data(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query')
        users = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        ).order_by('id')
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse({'users': user_list})
    return redirect('admin_dashboard_page')


# Logout
@never_cache
def logout_page(request):
    if 'username' or 'is_superuser' in request.session:
        logout(request)  
        request.session.flush()
    return redirect('login_page')
