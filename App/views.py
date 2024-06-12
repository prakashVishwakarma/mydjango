from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
# Create your views here.from django.http import JsonResponse
from .models import Post
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from .models import UserProfile, Address
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


#############   ONE TO ONE RELATIONSHIP   ##########################################################

def create_user_profile(request):
    if request.method == 'POST':
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Extract user and address data
        name = data.get('name')
        email = data.get('email')
        street = data.get('address', {}).get('street')
        city = data.get('address', {}).get('city')

        # Validate data (including email existence)
        errors = {}
        if not all([name, email, street, city]):
            errors['missing_fields'] = 'Missing required fields'
        if UserProfile.objects.filter(email=email).exists():
            errors['email_exists'] = 'Email address already exists'

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # Create UserProfile object
        user_profile = UserProfile.objects.create(name=name, email=email)

        # Create Address object if address data exists
        if street and city:
            address = Address.objects.create(user_profile=user_profile, street=street, city=city)
            user_profile.address = address
            user_profile.save()

        # Return serialized data (using dictionary)
        return JsonResponse({'name': user_profile.name, 'email': user_profile.email,
                             'address': {'street': user_profile.address.street, 'city': user_profile.address.city}})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
