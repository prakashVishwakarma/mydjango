from django.urls import path
from . import views

urlpatterns = [
    path('app/posts/', views.create_post, name='create_post'),
]
