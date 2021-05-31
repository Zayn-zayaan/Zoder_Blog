from django.urls import path, include
from blog.views import bloghome, blogpost, postComment, like_post, delete_post
from home.views import edit_blog

urlpatterns = [
            # API tompost comment
    path('postComment', postComment, name="postComment"),
    path('likes', like_post, name="like_post"),

    path('', bloghome, name='bloghome'), 
    path('<slug>/edit', edit_blog, name='edit_blog'),
    path('<slug>/', blogpost),
    path('<slug>/delete', delete_post)
    
]