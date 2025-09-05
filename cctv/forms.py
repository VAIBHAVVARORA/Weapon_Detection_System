# forms.py
from django import forms
from cctv.models import CCTVImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CCTVImage
        fields = ['image']
