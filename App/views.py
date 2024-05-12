from django.shortcuts import render, get_object_or_404

# Create your views here.from django.http import JsonResponse
from .models import Post
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
import json

def create_post(request):
    # Access data from request.POST dictionary
    title = request.POST.get('title')
    content = request.POST.get('content')

    # Validate data (optional, consider using Django forms for robust validation)
    if not title or not content:
        return JsonResponse({'error': 'Please provide title and content.'}, status=400)
    
    # Additional checks (optional)
    if len(title) < 3:
        return JsonResponse({'error': 'Title must be at least 3 characters long.'}, status=400)
    
    # Additional check for duplicate title in views.py (optional)
    try:
        existing_post = Post.objects.get(title=title)
        return JsonResponse({'error': 'Title already exists. Please choose a unique title.'}, status=400)
    except Post.DoesNotExist:
        # pass  # Proceed if title is unique
        
        # Create a new Post object
        post = Post.objects.create(title=title, content=content)

        # Serialize the Post object manually (without Django REST Framework serializers)
        response_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
        }
    

    return JsonResponse(response_data, status=201)

def get_all_posts(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),  # Convert datetime to ISO format
            "updated_at": post.updated_at.isoformat(),
        })
    return JsonResponse(data, safe=False)  # Allow for non-dictionary data

    post = get_object_or_404(Post, pk=post_id)
    data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
        "updated_at": post.updated_at.isoformat(),
    }
    return JsonResponse(data)