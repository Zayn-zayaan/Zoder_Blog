from django import forms
from django.forms import CharField, Form, PasswordInput
from blog.models import profile, Post
from django.contrib.auth.models import User

class create_profile_form(forms.ModelForm):
    
    class Meta:
        model = profile 
        exclude = ['user']

class userform(forms.ModelForm):
    pass2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    def clean_pass2(self):
        pass2 = self.cleaned_data.get("pass2")

        return pass2
    def save(self, commit=True):
        user = super(userform, self).save(commit=False)
        user.set_password(self.cleaned_data['pass2'])
        if commit:
            user.save()
        return user

class create_post_form(forms.ModelForm):
    
   
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'content',]


class Update_post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'content',]

    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.content = self.cleaned_data['content']
        blog_post.slug = self.cleaned_data['slug']

        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']

        if commit:
            blog_post.save()
        return blog_post
 
class update_dp_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['dp']
    def save(self, commit=True):
        acc_dp = self.instance
        if self.cleaned_data['dp']:
            acc_dp.dp = self.cleaned_data['dp']

        if commit:
            acc_dp.save()
        return acc_dp

class update_account_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']

    def save(self, commit=True):
        acc = self.instance
        acc.username = self.cleaned_data['username']
        acc.email = self.cleaned_data['email']
        if commit:
            acc.save()
        return acc

    
