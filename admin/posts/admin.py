from django.contrib import admin
from .models import Posts
# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Posts, PostsAdmin)
