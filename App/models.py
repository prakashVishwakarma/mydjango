# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError


def validate_title_length(value):
    min_length = 3  # Minimum allowed title length
    if len(value) < min_length:
        raise ValidationError(f"Title must be at least {min_length} characters long.")


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_title_length])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
