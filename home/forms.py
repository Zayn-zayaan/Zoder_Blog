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




 

    
    
