from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CareManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CareUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = [
        ('caretaker', 'Caretaker'),
        ('careseeker', 'Careseeker'),
    ]

    start_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField()
    firstname = models.TextField(max_length=60)
    lastname = models.TextField(max_length=60)
    age = models.IntegerField()
    gender = models.TextField()
    email = models.EmailField(max_length=254, unique=True)
    phone = models.BigIntegerField()
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="None")

    USERNAME_FIELD = 'email' # change username to email for authentication
    REQUIRED_FIELDS = ['firstname', 'lastname', 'age', 'gender', 'phone'] # can't be null

    objects = CareManager() # allow admin to manipulate this user

    def __str__(self):  # string representaion
        return self.email


class Caretaker(CareUser):
    experience = models.IntegerField()
    id_card_number = models.BigIntegerField()
    profession = models.TextField()
    objective = models.TextField(max_length=300)
    is_caretaker = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    @property
    def user_caretaker(self):
        return self.user_type == 'caretaker'


class Careseeker(CareUser):
    state = models.TextField(max_length=60)
    city = models.TextField(max_length=60)
    address = models.TextField(max_length=80)
    order = models.TextField(max_length=100)
    is_careseeker = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    @property
    def user_careseeker(self):
        return self.user_type == 'careseeker'


