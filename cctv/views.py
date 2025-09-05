from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cctv.forms import ImageUploadForm
from cctv.models import CCTVImage
from email.message import EmailMessage 
import ssl
import smtplib
# Create your views here.


@login_required(login_url='signin')
def about(request):
    return render(request, 'cctv/about.html')


@login_required(login_url='signin')
def contact(request):
    return render(request, 'cctv/contact.html')


@login_required(login_url='signin')
def webcam(request):
    return render(request, 'webcam.py')



@login_required(login_url='signin')
def home(request):
    email = request.user.email
    if request.method == 'POST':    
        email_sender = 'namdev2003satyam@gmail.com'
        email_password = 'erfjrmiajuyglgqf'
        email_receiver = email

        subject = 'Alert Mail!'
        body_content = 'This is a test email from Weapon Detection System'

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
    return render(request, 'cctv/home.html')



@login_required(login_url='signin')
def image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image')
    else:
        form = ImageUploadForm()
        
    images = CCTVImage.objects.all()

    processed_images = CCTVImage.objects.filter(processed_image__isnull=False)
    
    context = {'images': processed_images, 'form': form}
    return render(request, 'cctv/image.html', context)

# all_images = CCTVImage.objects.all()
# for image in all_images:
#     image.delete()

def delete_image(request):
    if request.method == 'POST':
        try:
            all_images = CCTVImage.objects.all()
            for image in all_images:
                image.delete()
            messages.success(request, 'All images deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    else:
        messages.error(request, 'No image selected for deletion.')

    return redirect('image')




    









