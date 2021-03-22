from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )
class Photo_Form(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description','tags')

class Photo_Extend_Form(forms.ModelForm):
    class Meta:
        model = Photo_Image
        fields = ('image',)