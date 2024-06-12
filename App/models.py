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

class UserProfile(models.Model):
    # User details
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Address(models.Model):
    # User address details
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
