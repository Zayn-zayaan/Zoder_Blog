from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView

from .models import Contact
from blog.models import profile
from django.contrib import messages
from blog.models import Post, profile
from.forms import create_profile_form, userform, create_post_form, Update_post_form, update_account_form, update_dp_form

from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD


import threading
from threading import Thread

class Emailthread(threading.Thread):

    def __init__(self, email):
        user_v = User.objects.get(email=email)
        self.user_v = user_v
        threading.Thread.__init__(self)

    def run(self):
        send_email(self.user_v)
=======
>>>>>>> 1f92c7e (added update and delete post functionality ,email verification ,account updatation etc.)

# HTML Pages

def home(request):
    context = {}
    posts   = Post.objects.filter().order_by('-views')[:2]
    context['posts'] = posts
    return render(request, 'home/home.html',context)
<<<<<<< HEAD

=======
    
>>>>>>> 1f92c7e (added update and delete post functionality ,email verification ,account updatation etc.)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        name  = request.POST['name']
        email = request.POST['email']
        phone = request.POST.get('phone', default=None)
        content = request.POST['content']
        if len(name) < 2 or len(email) < 4 or len(str(phone)) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly ")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allposts = Post.objects.none()
    else:
        allpoststitle = Post.objects.filter(title__contains=query)
        allpostscontent = Post.objects.filter(content__icontains=query)
        allposts = allpoststitle.union(allpostscontent)
    if allposts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query ")
    params = {'allposts': allposts, 'query':query}
    return render(request, 'home/search.html', params)

def createpost(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("404 not found")

    form = create_post_form(request.POST or None, request.FILES or None)
    context = {}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = user
        obj.save()
        form=create_post_form()
        messages.success(request, "Your post has been successfully created.")

    context['form'] = form
    return render(request, 'home/createpost.html', context)

# Authentication APIs
def handlesignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']


        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')

        # Create the user
        form = create_profile_form(request.POST or None, request.FILES or None)
        form1 = userform(request.POST)

        if form.is_valid() and form1.is_valid():
            f = form1.save(commit=False)
            f.first_name = fname
            f.last_name = lname
            f.save()
            obj = form.save(commit=False)
            obj.user = form1.save()   
            obj.save()

            user_verify = User.objects.get(email=email,username=username)
            user_verify.is_active = False
            send_email_task(user_verify)
            messages.error(request, "Your account has created. Please verify your email.We have emailed you a verification link. You will get that within 30 mins.")
            return redirect('home')

        else:
            form = create_profile_form()
            form1 = userform()

    else:
        return HttpResponse("404 - Not Found")

def handlelogin(request):
    if request.method == 'POST':
        # Get the Post parametres
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpassword)
        user_verify = User.objects.get(username=loginusername)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        elif user_verify.is_active == False:
            messages.error(request, "Please verify your email first to login.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials: Please try again")
            return redirect('home')
    return HttpResponse('404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def edit_blog(request, slug):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(Post, slug=slug)

    if blog_post.author != str(request.user):
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = Update_post_form(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            blog_post = obj
            messages.success(request, "Your post has been successfully updated")

    form = Update_post_form(
        initial={
            "title": blog_post.title,
            "slug": blog_post.slug,
            "content": blog_post.content,
            "image": blog_post.image,
        }
    )
    context['form'] = form
    return render(request, "blog/edit_blog.html", context)
<<<<<<< HEAD

def edituser(request):
    context = {}
    if not request.user.is_authenticated:
        messages.error(request, "must authenticate first")
        return redirect("home")
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        dp = request.POST.get('dp')

        if User.objects.filter(username=username).exists() and request.user.username != username:
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists() and request.user.email != email:
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')
        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')

        Post.objects.filter(author=str(request.user)).update(author=username)
        profile.objects.filter(username=str(request.user)).update(username=username)
        form = update_account_form(request.POST or None, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Your account has been successfully updated")

    form = update_account_form(
        initial={
            "email": request.user.email,
            "username": request.user.username,
        }
    )
    context['form'] = form
    return render(request, "home/edituser.html", context)

class custom_password_change(PasswordChangeView):
    template_name = 'home/change-password.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been succesfully updated")
        return super().form_valid(form)

@csrf_exempt
def sendEmail(request):
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user.is_active == False:
            Emailthread(email).start()
            messages.success(request, "Please verify your email.We have emailed you a verification link. You will get that within 30 mins.")
            return redirect('home')
        else:
            messages.success(request, "Your email is already verified")
            return redirect('home')
    return render(request, 'verify/verify_email.html')

=======

def edituser(request):
    context = {}
    if not request.user.is_authenticated:
        messages.error(request, "must authenticate first")
        return redirect("home")
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        dp = request.POST.get('dp')

        if User.objects.filter(username=username).exists() and request.user.username != username:
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists() and request.user.email != email:
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')
        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
            
        Post.objects.filter(author=str(request.user)).update(author=username)
        form = update_account_form(request.POST or None, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, "Your account has been successfully updated")

    form = update_account_form(
        initial={
            "email": request.user.email,
            "username": request.user.username,
        }
    )
    context['form'] = form
    return render(request, "home/edituser.html", context)

class custom_password_change(PasswordChangeView):
    template_name = 'home/change-password.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "Your password has been succesfully updated")
        return super().form_valid(form)

@csrf_exempt
def sendEmail(request):
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user.is_active == False:
            send_email(user)
            messages.success(request, "Please verify your email.We have emailed you a verification link.")
            return redirect('home')
        else:
            messages.success(request, "Your email is already verified")
            return redirect('home')
    return render(request, 'verify/verify_email.html')

>>>>>>> 1f92c7e (added update and delete post functionality ,email verification ,account updatation etc.)
def edit_dp(request):
    context={}
    if not request.user.is_authenticated:
        messages.error(request, "must authenticate first")
        return redirect("home")
<<<<<<< HEAD
    update_dp = get_object_or_404(profile, username=str(request.user))
=======
    update_dp = get_object_or_404(profile, username=request.user)
>>>>>>> 1f92c7e (added update and delete post functionality ,email verification ,account updatation etc.)

    if request.POST:
        form = update_dp_form(request.POST or None, request.FILES or None, instance = update_dp)
        if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                update_dp = obj
                messages.success(request, "Your profile picture has been successfully updated")
    form = update_dp_form(
        initial={
            "dp":update_dp.dp,
        }
    )
    context['form'] = form
    return render(request, "home/edit_dp.html", context)
