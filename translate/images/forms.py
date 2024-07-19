# forms.py
from django import forms
from .models import Webtoon


class WebtoonForm(forms.ModelForm):

    class Meta:
        model = Webtoon
        fields = ['name', 'webtoon_img']
