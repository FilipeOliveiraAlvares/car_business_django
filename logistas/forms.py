from django import forms
from garagens.models import Loja

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = [
            'nome',
            'endereco',
            'telefone',
            'logo',
            'cidade',
            'whatsapp',
            'instagram',
            'facebook',
            'site',
            'maps_url',
        ]

        widgets = {
            'endereco': forms.TextInput(attrs={'placeholder': 'Rua, número, bairro...'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(99) 99999-9999'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': '(99) 99999-9999 ou 5599999999999'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'https://instagram.com/sualoja'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'https://facebook.com/sualoja'}),
            'site': forms.URLInput(attrs={'placeholder': 'https://www.sualoja.com'}),
            'maps_url': forms.URLInput(attrs={'placeholder': 'Cole aqui o link do Google Maps'}),
        }
