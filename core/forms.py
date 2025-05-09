from django import forms
from .models import Paper, Poster, FAQ

class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['title', 'author']


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'pdf', 'editor_comments', 'reviewer_comments']


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']