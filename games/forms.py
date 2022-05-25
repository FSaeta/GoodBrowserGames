from django import forms

from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        fields = ['comentario']
        model = Avaliacao
        widgets = {
            'comentario': forms.Textarea(attrs={'style': 'resize: none;'}),
        }
        labels = {
            'comentario': ''
        }

class NewAvaliacaoForm(forms.ModelForm):
    class Meta:
        fields = ['comentario', 'rating', 'user', 'game']
        model = Avaliacao
        widgets = {
            'comentario': forms.Textarea(attrs={'style': 'resize: none;'}),
        }
        labels = {
            'comentario': ''
        }
