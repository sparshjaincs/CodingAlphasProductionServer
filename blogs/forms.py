from django import forms

from Core.models import *

class Article_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write your title here ...",'style':'font-size:36px;'}))
    tags = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write comma (,) seperated tags here ...",'style':'font-size:14px;'}))
    
    class Meta:
        model = Articles
        fields = ('title','image','tags','content')