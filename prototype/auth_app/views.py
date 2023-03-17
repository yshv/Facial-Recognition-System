from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser

# Create your views here.

from django.http import JsonResponse

def facial_auth(request):
    if request.method == 'POST':
        # Retrieve the facial data from the request
        facial_data = request.POST.get('facial_data', None)

        # Save the facial data to the user's profile
        if facial_data:
            request.user.facial_data = json.loads(facial_data)
            request.user.save()

        return JsonResponse({'status': 'success'})

    return render(request, 'facial_auth.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        facial_data = request.POST.get('facial_data', None)  # Add this line
        
        # Check if passwords match
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        # Check if user with the same email already exists
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email is already taken'})
        
        # Check if user with the same username already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username is already taken'})
        
        # Create new user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, facial_data=facial_data)
        user.save()
        
        # Redirect to login page
        return redirect('login')
    
    # Render the signup form if the request method is GET
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        facial_data = request.POST.get('facial_data', None)

        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                if facial_data:
                    # Perform facial authentication
                    # If the facial authentication fails, show an error message and redirect to the login page.
                    # Otherwise, proceed with the login.
                    pass
                auth_login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('facial_auth')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('facial_auth')  # Replace 'main_page' with the name of the view for your main page.

