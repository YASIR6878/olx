from collections import UserDict
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse 

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.hashers import make_password
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout,get_user_model

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from item.models import Item,Category

def index(request):
    if request.user.is_anonymous:
        return redirect('loginuser')
    else:
        items=Item.objects.filter(is_sold=False)[0:20]
        category=Category.objects.all()
        context={
            'items':items,
            'categories':category
        }
        return render(request,'index.html',context)
def loginuser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('pass1')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect('loginuser')
    else:
       return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('loginuser')

def signup(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pass1 = form.cleaned_data['pass1']
            pass2 = form.cleaned_data['pass2']

            if pass1 == pass2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'User Already Exists')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Account Already Exists')
                    return redirect('signup')
                else:
                    # Create a UserRegistration instance
                    hashed_password = make_password(pass1)
                    user = User(username=username, email=email, password=hashed_password)
                    user.is_active = False
                    user.save()

                    # Generate and set the confirmation token
                    token = account_activation_token.make_token(user)
                    user.confirmation_token = token
                    user.save()
                    messages.success(request,'Check your email for confirmation instructions.')
                    # Send the confirmation email
                    activateEmail(request,user,email)
            else:
                messages.info(request, 'Password Not Matching!')
                return redirect('signup')
    else:
        form = ContactForm()
    return render(request, 'signup.html', {'form': form})

def activateEmail(request,user,to_email):
    subject='Confirm Your Signup'
    message=render_to_string('template_activate_account.html',{
        'user':user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        "protocol":'https' if request.is_secure()else 'http'
    })
    email=EmailMessage(subject,message,to=[to_email])
    if email.send():
       messages.success(request,f'Dear <b>{user}<b>,Please check your email <b>{to_email}<b>for Confirmation.')
    else:
        messages.error(request,'Check Your Email again!')

from django.contrib import messages

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully. You can now log in.')
        return redirect('loginuser')
    else:
        messages.error(request, 'Activation Link is Expired or invalid.')
        return redirect('signup')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        user_email = request.POST['email']
        message = request.POST['message']

        # Create an EmailMessage instance
        email = EmailMessage(
            'User Review',
            f'Name: {name}\nEmail: {user_email}\nMessage: {message}',
            user_email,
            ['yasirmanzoor6878@gmail.com'],  # Receiver
        )

        # Send the email
        email.send()
    return render(request, 'contact.html')



def filterbystates(request):
     if request.user.is_anonymous:
       return redirect('loginuser')
     else:
        if request.method == 'GET':
            stateselected = request.GET.get('state').lower()
            stateitem = Item.objects.filter(state=stateselected)
            return render(request, 'state.html', {'stateitem': stateitem})
        else:
            return render(request, 'state.html')