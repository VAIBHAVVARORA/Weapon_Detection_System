from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cctv.forms import ImageUploadForm
from cctv.models import CCTVImage
# Create your views here.


@login_required(login_url='signin')
def about(request):
    return render(request, 'cctv/about.html')


@login_required(login_url='signin')
def contact(request):
    return render(request, 'cctv/contact.html')


@login_required(login_url='signin')
def webcam(request):
    return render(request, 'cctv/webcam.html')



from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='signin')
def home(request):
    email = request.user.email
    if request.method == 'POST':    
        subject = 'Alert Mail!'
        body_content = 'This is a test email from Weapon Detection System'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        
        try:
            send_mail( subject, body_content, email_from, recipient_list )
            messages.success(request, 'Email sent successfully !')
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')
    return render(request, 'cctv/home.html')



from django.views.decorators.cache import never_cache

@never_cache
@login_required(login_url='signin')
def image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            
            # Check for detections and send email
            if instance.prediction and instance.prediction != "No detections":
                subject = 'WEAPON DETECTED ALERT!'
                email_from = settings.EMAIL_HOST_USER
                email_to = [request.user.email]
                
                body = f"""
                ALERT: A weapon has been detected in an uploaded image.
                
                Detected Item(s): {instance.prediction}
                Time: {instance.uploaded_at}
                User: {request.user.username}
                
                Please take immediate action.
                """
                
                try:
                    send_mail(subject, body, email_from, email_to, fail_silently=False)
                    messages.warning(request, f'Weapon Detected! Alert email sent to {request.user.email}')
                except Exception as e:
                    messages.error(request, f'Weapon Detected but failed to send email: {e}')
            
            return redirect('image')
    else:
        form = ImageUploadForm()
        
    # Show all images, ordered by newest first
    processed_images = CCTVImage.objects.filter(processed_image__isnull=False).order_by('-uploaded_at')
    
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




    









