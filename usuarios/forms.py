from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import PerfilUsuario

class EditarPerfilForm(forms.ModelForm):
    """Formulário para editar perfil do usuário"""
    username = forms.CharField(
        label="Nome de usuário",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nome de usuário'
        })
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'seu@email.com'
        })
    )
    first_name = forms.CharField(
        label="Primeiro nome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seu primeiro nome'
        })
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seu sobrenome'
        })
    )

    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'foto']
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '(00) 00000-0000'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            })
        }
        labels = {
            'telefone': 'Telefone',
            'foto': 'Foto de perfil'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.usuario:
            self.fields['username'].initial = self.instance.usuario.username
            self.fields['email'].initial = self.instance.usuario.email
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.user and User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if commit:
            perfil.save()
            # Atualiza dados do User
            user = perfil.usuario
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return perfil


class AlterarSenhaForm(PasswordChangeForm):
    """Formulário para alterar senha"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Senha atual'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Nova senha'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirmar nova senha'
        })

