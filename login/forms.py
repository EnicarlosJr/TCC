# login/forms.py
from django import forms
from login.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """
    Formulário personalizado para criação de usuários.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'tipo_usuario']

    username = forms.CharField(
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Digite o nome de usuário',
            'required': True,
        })
    )

    email = forms.EmailField(
        label="Email Institucional",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'placeholder': 'Digite o email @ufvjm.edu.br',
            'required': True,
        })
    )

    tipo_usuario = forms.ChoiceField(
        label="Tipo de Usuário",
        choices=[
            ('farmaceutico', 'Farmacêutico'),
            ('aluno', 'Aluno'),
            ('convidado', 'Convidado')
        ],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
            'required': True,
        })
    )
