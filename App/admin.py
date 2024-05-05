from django.contrib import admin
from App.models import Post
# Register your models here.

@admin.register(Post)
class CrudAdmin(admin.ModelAdmin):
    list_display = ('title','content',)

# admin.site.register(Post, CrudAdmin)