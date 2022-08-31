from django import forms
from django.contrib.auth import authenticate
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

    def clean(self):
        res = super(LoginForm, self).clean()

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError(
                'Los datos de usuarios no son correctos.'
            )

        return res


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password actual'
            }
        )
    )

    password2 = forms.CharField(
        label='password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Nueva password'
            }
        )
    )

    # def clean(self):
    #     res = super(UpdatePasswordForm, self).clean()

    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']

    #     if not authenticate(username=username, password=password):
    #         raise forms.ValidationError(
    #             'Los datos de usuarios no son correctos.'
    #         )

    #     return res


class VerificationForm(forms.Form):
    coderegistro = forms.CharField(required=True, max_length=6)

    def __init__(self, pk, *args, **kwargs):
        # metodo que se ejecuta cuando se inicializa un formulario

        self.id_user = pk

        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_coderegistro(self):
        # id_user = self.kwargs['pk']

        codigo = self.cleaned_data['coderegistro']

        if len(codigo) == 6:
            # verificamos si el codigo y el id de usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError(
                    'El codigo es incorrecto.'
                )
        else:
            raise forms.ValidationError(
                'El codigo es incorrecto.'
            )
