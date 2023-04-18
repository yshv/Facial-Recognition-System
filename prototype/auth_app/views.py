from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from .models import CustomUser
import json
import random
import pymongo
import bcrypt
import sys
import time
sys.path.append('..')
from face_liveness_identification.face_recognition_liveness_app import recognition_liveness
from face_liveness_identification.encode_faces import encode_faces
# Create your views here.

from django.http import JsonResponse

def facial_auth(request):
    # session_keys = list(request.session.keys())
    # # Delete each session key
    # if session_keys:
    #     for key in session_keys:
    #         del request.session[key]
    if request.method == 'POST':
        # Retrieve the facial data from the request
        facial_data = request.POST.get('facial_data', None)

        # Save the facial data to the user's profile
        if facial_data:
            request.user.facial_data = json.loads(facial_data)
            request.user.save()

        return JsonResponse({'status': 'success'})

    return render(request, 'facial_auth.html')

# Create a dictionary to store the last request time for each IP address
signup_request_times = {}
def signup(request):
    if request.method == 'POST':
        client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
        db = client.admin
        email = request.POST['email']
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        vstep_status = 'default'
        vstep_info = 'default'
        facial_data = request.POST.get('facial_data')
        if facial_data is None:
            return render(request, 'signup.html', {'error': 'Facial data is not provided'})
        else:
            encoded_facial_data = encode_faces(facial_data, username)
            # encoded_facial_data['encodings'] = encoded_facial_data['encodings'].tolist()
        
        db = client.customers
        customers = db.customers

        # rate limiting
        # Get the IP address of the client
        ip_address = request.META.get('REMOTE_ADDR')
        # Check if the IP address is already in the dictionary
        if ip_address in signup_request_times:
            # Get the last request time for the IP address
            last_request_time = signup_request_times[ip_address]

            # Calculate the time elapsed since the last request
            current_time = time.time()
            time_elapsed = current_time - last_request_time

            # If the time elapsed is less than 60 seconds, return an error response
            if time_elapsed < 60:
                return render(request, 'signup.html', {'error': 'Too many requests. Please try again later.'})

        # Update the last request time for the IP address
        signup_request_times[ip_address] = time.time()
        
        if customers.count_documents({'email': email}) != 0:
            return render(request, 'signup.html', {'error': 'Email is already taken'})
        if customers.count_documents({'username': username}) != 0:
            return render(request, 'signup.html', {'error': 'Username is already taken'})
        customer = {'email': email, 'username': username, 'password': password, 'vstep_status': vstep_status, 'vstep_info': vstep_info, 'facial_data': encoded_facial_data}
        print(customer)
        db.customers.insert_one(customer)
        # Redirect to login page
        return redirect('login')
    
    # Render the signup form if the request method is GET
    return render(request, 'signup.html')

def login(request):
    print(request.session.keys())
    if request.method == 'POST':
        client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
        db = client.admin
        db = client.customers
        customers = db.customers
        email = request.POST.get('email')
        password = request.POST.get('password')
        # facial_data = request.POST.get('facial_data', None)
        if customers.count_documents({'$and': [{'email': email}]}):
            data = list(customers.find({'$and': [{'email': email}]}))
            # print(data)
            hashed_password = data[0]['password']
            username = data[0]['username']
            facial_data = data[0]['facial_data']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                name, label_name = recognition_liveness('liveness.model', 'label_encoder.pickle', 
                                            'face_detector', facial_data, confidence=0.5)
                print(name, label_name)
                if name != username:
                    return render(request, 'login.html', {'error': 'Wrong person.'})
                elif label_name != 'real':
                    return render(request, 'login.html', {'error': 'Spoofing detected.'})
                elif name == username and label_name == 'real':
                    messages.success(request, 'Login successfully.')
                    request.session['email'] = email
                    request.session['password'] = hashed_password
                    print(hashed_password)
                    return redirect('umain')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password.'})

    return render(request, 'login.html')
    
def umain(request):
    email = request.session.get('email')
    password = request.session.get('password')
    if request.method == 'POST':
        print(request.POST)
        if 'settings' in request.POST.keys():
            print('go to settings')
            return redirect('settings')
        pass
        
        return redirect('umain')
    else:
        return render(request, 'umain.html')
    
def settings(request):
    email = request.session.get('email')
    password = request.session.get('password')
    client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
    db = client.admin
    db = client.customers
    customers = db.customers
    data = list(customers.find({'$and': [{'email': email}, {'password': password}]}))
    context = {'data': data[0]}
    if request.method == 'POST':
        print('receive request')
        key_info = list(request.POST.keys())
        print(key_info)
        if key_info:
            print(key_info[1])
            if 'edit'in key_info[1]:
                request.session['action'] = key_info[1][:4]
                request.session['type'] = key_info[1][5:]
                request.session['vstep_status_change'] = 'False'
                if data[0]['vstep_status'] == 'Enable':
                    return redirect('vstep')
                else:
                    return redirect('editordel')
            elif 'delete' in key_info[1]:
                request.session['action'] = key_info[1][:6]
                request.session['type'] = key_info[1][7:]
                request.session['vstep_status_change'] = 'False'
                if data[0]['vstep_status'] == 'Enable':
                    return redirect('vstep')
                else:
                    return redirect('editordel')
            elif 'able' in key_info[1]:
                if data[0]['vstep_info'] == 'default':
                    return redirect('vstep_init')
                request.session['vstep_status'] = data[0]['vstep_status']
                request.session['vstep_info'] = data[0]['vstep_info']
                request.session['vstep_status_change'] = 'True'
                return redirect('vstep')
        return redirect('settings')
    else:
        return render(request, 'settings.html', context)
    
def vstep_init(request):
    email = request.session.get('email')
    password = request.session.get('password')
    
    client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
    db = client.admin
    db = client.customers
    customers = db.customers
    data = list(customers.find({'$and': [{'email': email}, {'password': password}]}))

    if request.method == 'POST':
        print('get_post')
        vstep_status = 'Enable'
        vstep_info = request.POST.get('vstep_info')
        context = {'confirm': ''}
        print(request.session.keys())
        if ('vcode' in request.POST.keys()):
            if 'vcode' not in request.session.keys():
                request.session['vcode'] = 'unused'
            if (request.session['vcode']!='used'):
                print('get_vcode')
                subject = 'Verification' # Replace with your email subject
                code = str(random.randint(100000, 999999))
                request.session['code'] = code
                message = 'Verification code: ' + code # Replace with your email body
                from_email = 'sec_group13@outlook.com' # Replace with your Gmail email address
                recipient_list = [vstep_info] # Replace with the recipient's email address
                send_mail(subject, message, from_email, recipient_list)
                request.session['vstep_init_info'] = vstep_info
                request.session['vcode'] = 'used'
                context['confirm'] = request.session['vcode']
                return render(request, 'vstep_init.html', context)
            else:
                request.session['vcode'] = 'unused'
                return redirect('vstep_init')
        if 'vconfirm' in request.POST.keys():
            print('get_vconfirm')
            request.session['vcode'] = 'unused'
            verification_code = request.POST.get('verification_code')
            if verification_code == request.session['code']:
                customers.update_one({'email': email, 'password': password}, {'$set': {'vstep_status': vstep_status, 'vstep_info': request.session['vstep_init_info']}})
                request.session['vstep_status'] = vstep_status
                request.session['vstep_info'] = request.session['vstep_init_info']
                request.session['vstep_status_change'] = 'False'
            return redirect('settings')
        print(context)
        return redirect('vstep_init')
    
    return render(request, 'vstep_init.html')

def vstep(request):
    email = request.session.get('email')
    password = request.session.get('password')
    
    client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
    db = client.admin
    db = client.customers
    customers = db.customers
    data = list(customers.find({'$and': [{'email': email}, {'password': password}]}))
    context = {'confirm': ''}
    if request.method == 'POST':
        vemail = request.POST.get('email')
        print(request.POST.keys())
        print(request.session.keys())
        if 'vcode' in request.POST.keys():
            if 'vcode' not in request.session.keys():
                request.session['vcode'] = 'unused'
            if (request.session['vcode']!='used'):
                if vemail != data[0]['vstep_info']:
                    return render(request, 'vstep.html', {'error': 'Input email is not the same as your secondary email.'})
                subject = 'Verification' # Replace with your email subject
                code = str(random.randint(100000, 999999))
                request.session['code'] = code
                message = 'Verification code: ' + code # Replace with your email body
                from_email = 'sec_group13@outlook.com' # Replace with your Gmail email address
                recipient_list = [vemail] # Replace with the recipient's email address
                send_mail(subject, message, from_email, recipient_list)
                request.session['vcode'] = 'used'
                context['confirm'] = request.session['vcode']
                return render(request, 'vstep.html', context)
            else:
                request.session['vcode'] = 'unused'
                return redirect('vstep')
        if 'vconfirm' in request.POST.keys():
            request.session['vcode'] = 'unused'
            verification_code = request.POST.get('verification_code')
            if verification_code == request.session['code']:
                if request.session['vstep_status_change'] == 'True':
                    if data[0]['vstep_status'] == 'Enable':
                        customers.update_one({'email': email, 'password': password}, {'$set': {'vstep_status': 'Disable'}})
                        return redirect('settings')
                    else:
                        customers.update_one({'email': email, 'password': password}, {'$set': {'vstep_status': 'Enable'}})
                        return redirect('settings')
                return redirect('editordel')
            context['confirm'] = request.session['vcode']
            return render(request, 'vstep.html', context)
        print(context)
        return redirect('vstep')
    
    return render(request, 'vstep.html')

def editordel(request):
    action = request.session['action']
    action_type = request.session['type']
    email = request.session.get('email')
    password = request.session.get('password')
    data = {'action': action, 'type': action_type}
    context = {'data': data}
    print(context)
    if request.method == 'POST':
        if 'update' in request.POST.keys():
            modified_info = request.POST.get('info1')
            modified_info_conf = request.POST.get('info2')
            client = pymongo.MongoClient('mongodb+srv://admin:admin@security.ju0aixd.mongodb.net/?retryWrites=true&w=majority')
            db = client.admin
            db = client.customers
            customers = db.customers
            # Find document to be modified
            document = customers.find_one({'email': email, 'password': password})
            
            if document:
                if action == 'edit':
                    if modified_info != modified_info_conf:
                        print('donot match')
                        return render(request, 'editordel.html', {'error': 'Two inputs do not match.', 'data': data})      
                    if action_type == 'password':
                        modified_info = bcrypt.hashpw(modified_info.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    customers.update_one({'email': email, 'password': password}, {'$set': {action_type: modified_info}})
                if action == 'delete':
                    if modified_info != email or not bcrypt.checkpw(modified_info_conf.encode('utf-8'), password.encode('utf-8')):
                        return render(request, 'editordel.html', {'error': 'Invalid email or password.', 'data': data})
                    customers.delete_one({'email': email, 'password': password})
            return redirect('login')
        return redirect('settings')
    
    return render(request, 'editordel.html', context)




from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('facial_auth')  # Replace 'main_page' with the name of the view for your main page.

