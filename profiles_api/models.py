from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manage for user profiles"""

    def creat_user(self, email, name, password=None):
        """Creat a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email) #my=>cuse of some part of email address is case sensetive , try to be is normal form all emails.
        user = self.model(email=email,name=name)

        user.set_password(password) #my=>we want to be sour that the pass is convert to hash and never save to databases as plaintext.
        user.save(using=self._db) #my=>(using=self._db) for suporting each database type.

        return user

    def creat_superuser(self, email, name, password):
        """Creat save a new superuser with given details"""
        user = self.creat_user(email, name, password)

        user.is_superuser = True #my=>it's comes from PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' #my=>user name is required so we say to django take email as username
    REQUIRED_FIELDS = ['name'] #my=>user name is here by default so email is requireds.

    def get_full_name(self):
        """Retrive full name of user"""
        return self.name

    def get_short_name(self):
        """Retrive full name of user"""
        return self.name

        def __str__(self): #my=>this is recommended for all django models.
            """Return string representation of our user"""
            return self.email
