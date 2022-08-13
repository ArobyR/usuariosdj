from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    
    # def create_user(self):
    #     """ overwriting crate_user """
    #     pass
    
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """ is_staff and is_superuser are from another Model AbstractBaseUser """
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        
        user.set_password(password) # hash the password
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """ overwriting create_superuser """
        return self._create_user(username, email, password, True, True, **extra_fields)