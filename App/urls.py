from django.urls import path
from . import views

urlpatterns = [
    path('app/posts/', views.create_post, name='create_post'),
    path('posts/', views.get_all_posts, name='all_posts'),
    path('posts/<int:post_id>/', views.get_post_by_id, name='post_detail'),
    path('delete_posts/<int:post_id>/', views.delete_post, name='delete_post'),
]
