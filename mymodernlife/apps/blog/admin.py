from django.contrib import admin

from models import *
    
class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)
    
class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)
