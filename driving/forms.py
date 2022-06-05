from django import forms
from django.forms import ModelForm

from driving.models import Src


class SrcForm(forms.Form):
    """出発地のフォーム"""
    src = forms.CharField(label='出発地', max_length=255,
                          widget=forms.TextInput(
                              attrs={'placeholder': '名称、座標どちらでも可', 'class': 'form-control col-xl'}))

class destForm(forms.Form):
    """目的地のフォーム"""
    name  = forms.CharField(label='目的地', max_length=255)
    highway = forms.CharField(label='高速の距離', max_length=255)
    localway = forms.CharField(label='下道の距離', max_length=255)
    latitude = forms.CharField(label='緯度', max_length=255)
    longitude = forms.CharField(label='経度', max_length=255)
    
