from django.contrib import admin
from django.urls import path
from cctv import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home", views.home, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("image", views.image, name='image'),
    path("about", views.about, name='about'),
    path("delete_image", views.delete_image, name='delete_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)