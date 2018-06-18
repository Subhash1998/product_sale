from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm,Textarea
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserProfile,Product


class UserForm(forms.ModelForm):
  first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
  class Meta:
  	model=User
  	fields=('first_name','email','username','password')


class EditAddress(forms.ModelForm):
      class Meta:
           model=UserProfile
           fields=('address',)


class EditMobile(forms.ModelForm):
      email=forms.EmailField()
      first_name=forms.CharField(max_length=200)
      address=forms.CharField(max_length=1000)
      class Meta:
           model=UserProfile
           fields=('mobile','address')

class EditImage(forms.ModelForm):
      class Meta:
           model=UserProfile
           fields=('image',)

class SearchForm(forms.ModelForm):
      class Meta:
           model=Product
           fields=('p_name','p_price',)

