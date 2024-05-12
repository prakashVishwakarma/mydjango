from django.contrib import admin
from django.urls import path, include
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('App.urls')),  # Assuming your app is named 'App'
]