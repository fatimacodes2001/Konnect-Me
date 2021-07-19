# forms.py
from django import forms
from .models import *

albums = Album.objects.all();

class TestForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Photos
        fields = ['caption','status_id','album']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name']


class PhotoForm(forms.ModelForm,):

    def __init__(self,CHOICES,*args,**kwargs):

        super(PhotoForm,self).__init__(*args,**kwargs)

        self.fields['photo'] = forms.ImageField()
        self.fields['album_id'] = forms.ChoiceField(choices = CHOICES)

    class Meta:
        model = Photos
        fields = ['caption','city','state']

class GeeksForm(forms.ModelForm):
    class Meta:
        model = GeeksModel
        fields = ['img']