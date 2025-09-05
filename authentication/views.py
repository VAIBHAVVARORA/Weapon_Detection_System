from django.contrib.auth.hashers import make_password
from email.message import EmailMessage
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
import ssl,smtplib,random

# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass']
        cpassword = request.POST['cpass']

        otp = str(random.randint(100000, 999999))


        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            request.session['signup_data'] = {
            'username': username,
            'fname': fname,
            'lname': lname,
            'email': email,
            'password': password,
            'otp' : otp
        }
            email_sender = 'namdev2003satyam@gmail.com'
            email_password = 'erfjrmiajuyglgqf'
            email_receiver = email

            subject = 'Verify Email!'
            body_content = f'Your One time password for Registration in ArgusVision is : {otp}. '

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body_content)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            messages.success(request, 'Email sent successfully !')
            
            return render(request, 'authentication/verify_otp.html')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
    return render(request, 'authentication/register.html')


def verify_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp', '')
        stored_otp = request.session.get('signup_data', {}).get('otp', '')
        print(user_entered_otp,stored_otp)
        if user_entered_otp == stored_otp:
            signup_data = request.session.get('signup_data', {})
            username = signup_data.get('username', '')
            fname = signup_data.get('fname', '')
            lname = signup_data.get('lname', '')
            email = signup_data.get('email', '')
            password = signup_data.get('password', '')

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, 'Account created successfully')

            # Remove signup data from session
            del request.session['signup_data']

            return redirect('signin')

        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'authentication/verify_otp.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('signin')

    return render(request, 'authentication/signin.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('signin')


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid() and form.cleaned_data['email'] != '' and User.objects.filter(email=form.cleaned_data['email']).exists():
            
            otp = str(random.randint(100000, 999999))
            email_sender = 'namdev2003satyam@gmail.com'
            email_password = 'erfjrmiajuyglgqf'
            email_receiver = request.POST['email']

            subject = 'PASSWORD RESET'
            body_content = f'Your One time password for PASSWORD RESET in ArgusVision is : {otp}. '

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body_content)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            messages.success(request, 'Password reset email sent successfully. Check your mail for OTP.')

            user = User.objects.filter(email=form.cleaned_data['email'])        
            user.password = make_password(otp)
            print(user)
            print(user.password)

            return redirect('signin')
        else:
            messages.error(request, 'Invalid email address.')
            form = PasswordResetForm()
    else:
        form = PasswordResetForm()

    return render(request, 'authentication/password_reset.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_entry(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            user_to_delete = User.objects.get(username=username)
            user_to_delete.delete()
            messages.success(request, "Successfully deleted user")
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('delete_entry')
    return render(request, 'authentication/delete_entry.html')
