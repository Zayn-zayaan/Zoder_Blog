from django.contrib import admin
from blog.models import Post, BlogComment, postviews, profile, usercount

# Register your models here.
admin.site.register(BlogComment)
admin.site.register(postviews)
admin.site.register(profile)
admin.site.register(usercount)
admin.site.register(Post)

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     class Media:
#         js = ('tinyinject.js',)
