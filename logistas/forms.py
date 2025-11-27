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
    
    def clean_instagram(self):
        """Valida e normaliza URL do Instagram"""
        instagram = self.cleaned_data.get('instagram', '').strip()
        if instagram and not instagram.startswith(('http://', 'https://')):
            # Se não começar com http, adiciona https://
            if instagram.startswith('@'):
                instagram = f'https://instagram.com/{instagram[1:]}'
            elif instagram:
                instagram = f'https://{instagram}'
        return instagram if instagram else None
    
    def clean_facebook(self):
        """Valida e normaliza URL do Facebook"""
        facebook = self.cleaned_data.get('facebook', '').strip()
        if facebook and not facebook.startswith(('http://', 'https://')):
            # Se não começar com http, adiciona https://
            facebook = f'https://{facebook}'
        return facebook if facebook else None
