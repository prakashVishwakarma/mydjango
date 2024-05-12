from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

# Create your views here.from django.http import JsonResponse
from .models import Post
from django.http import JsonResponse, Http404, HttpResponse

from django.shortcuts import get_object_or_404
import json


def create_post(request):
    # Access data from request.POST dictionary
    title = request.POST.get('title')

    # Validate data (optional, consider using Django forms for robust validation)
    if not title:
        return JsonResponse({'error': 'Please provide title. '}, status=400)

    content = request.POST.get('content')

    if not content:
        return JsonResponse({'error': 'Please provide content.'}, status=400)

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

    if not posts.exists():
        # No data found in database, send informative message
        return JsonResponse({'message': 'There are currently no posts available. Data is being mined!'})

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


def get_post_by_id(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat(),
        }
        return JsonResponse(data)
    except Http404:
        # Post not found, send informative message
        return JsonResponse({'message': 'Post with ID {} not found.'.format(post_id)})


def delete_post(request, post_id):
    try:
        # Check if Post with the given ID exists
        if not Post.objects.filter(pk=post_id).exists():
            raise ObjectDoesNotExist('Post with ID {} does not exist.'.format(post_id))

        post = Post.objects.get(pk=post_id)
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully.'})

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Handle other errors


def patch_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method != 'PATCH':
        return HttpResponse(status=405)  # Method Not Allowed

    try:
        data = json.loads(request.body)  # Parse request body as JSON
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # Update specific fields based on request data
    for field, value in data.items():
        if field not in ('title', 'content'):
            return JsonResponse({'error': 'Invalid field name'}, status=400)

        # Validation for title length
        # if field == 'title' and not validate_title_length(value):
        #     return JsonResponse({'error': 'Title length invalid'}, status=400)

        setattr(post, field, value)

    post.save()
    return JsonResponse({'message': 'Post updated successfully'}, status=200)
