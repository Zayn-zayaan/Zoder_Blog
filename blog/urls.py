from django.urls import path, include
from blog.views import bloghome, blogpost, postComment, like_post

urlpatterns = [
            # API tompost comment
    path('postComment', postComment, name="postComment"),
    path('likes', like_post, name="like_post"),

    path('', bloghome), 
    path('<str:slug>', blogpost),
    

]