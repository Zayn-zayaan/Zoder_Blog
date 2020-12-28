from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from ckeditor.fields import RichTextField

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dp   = models.ImageField(upload_to='images')

    def __str__(self):
        return self.user.username

@receiver(post_delete, sender=profile)
def submission_delete(sender, instance, **kwargs):
    instance.dp.delete(False)
    

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Post(models.Model):
    Sno      = models.AutoField(primary_key=True)
    title    = models.CharField(max_length=100)
    content  = RichTextField(blank=True, null=True)
    author   = models.CharField(max_length=100)
    slug     = models.SlugField(max_length=100)
    likes    = models.ManyToManyField(User, related_name='likes', blank=True)
    image    = models.ImageField(upload_to='images', default='images/usr.png')
    views    = models.IntegerField(default=0)
    date     = models.DateTimeField(blank=True, auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' by ' + self.author

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class BlogComment(models.Model):
        Sno        = models.AutoField(primary_key=True)
        comment    = models.TextField()
        user       = models.ForeignKey(User, on_delete=models.CASCADE)
        post       = models.ForeignKey(Post, on_delete=models.CASCADE)
        parent     = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
        timestamp  = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return self.comment[0:13] + "..." + "by " + self.user.username

class postviews(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    views = models.PositiveIntegerField(default=0)
    user  = models.CharField(max_length=100)
    def __str__(self):
        return self.post.title + " (" + str(self.views) + ") "

class usercount(models.Model):
    user  = models.CharField(max_length=100, default=None)
    def __str__(self):
        return self.user
    



