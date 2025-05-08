from django import forms
from .models import Poster

class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['title', 'author']