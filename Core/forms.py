from django import forms
from .models import *
class Photo_Form(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description','tags')

class Photo_Extend_Form(forms.ModelForm):
    class Meta:
        model = Photo_Image
        fields = ('image',)