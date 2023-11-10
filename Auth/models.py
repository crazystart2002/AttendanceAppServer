from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, name, role, email, password=None, password2=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
            role=role,
        )
        user.set_password(password)

        user.save(using=self.db)
        return user

    def create_superuser(self, username, name, role, email, password=None, password2=None):
        user = self.create_user(
            username,
            email=email,
            password=password,
            password2=password2,
            name=name,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        unique=True,
        max_length=8,
    )
    name = models.CharField(max_length=255)
    role = models.BooleanField()
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'role', 'email']

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, perm):
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user member of Staff?"
        return self.is_admin