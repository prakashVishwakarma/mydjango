# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


def validate_title_length(value):
    min_length = 3  # Minimum allowed title length
    if len(value) < min_length:
        raise ValidationError(f"Title must be at least {min_length} characters long.")


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_title_length])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#############   ONE TO ONE RELATIONSHIP   ##########################################################

class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.username


class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    interests = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.account.username}'s Profile"
