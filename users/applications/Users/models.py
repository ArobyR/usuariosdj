import imp
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """El abstract ya trae el field password
    """
    
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    
    username = models.CharField('Username', max_length=20, unique=True)
    email = models.EmailField('email', max_length=254)
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    # si queremos que x usuario pueda acceder al admintrador (es obligatorio definirlo)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['email',]
    
    objects = UserManager()
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
    