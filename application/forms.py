# forms.py
from django import forms
from .models import *

class TestForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Photos
        fields = ['caption','status_id','album']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name']

class PhotoForm(forms.ModelForm):
    photo = forms.ImageField()
    class Meta:
        model = Photos
        fields = ['caption']
