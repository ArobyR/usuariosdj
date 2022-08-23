from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password'
            }
        )
    )

    password2 = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'repit password'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "nombres",
            "apellidos",
            "genero",
        )

    # validator
    def clean_password2(self):
        if str(self.cleaned_data['password1']) != str(self.cleaned_data['password2']):
            self.add_error('password1', 'Las contrasenia no son iguales')
        
        # if len(self.cleaned_data['password1']) < 5:
        #     self.add_error(
        #         'password1',
        #         'La contrasenia debe ser mayor a 5 cinco digitos'
        #     )
        
class LoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'style': '{margin: 10px}',
            }
        )
    )
    
    password = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password'
            }
        )
    )
