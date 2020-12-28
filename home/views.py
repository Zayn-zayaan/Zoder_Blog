from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from .models import Contact
from django.contrib import messages
from blog.models import Post, profile
from.forms import create_profile_form, userform, create_post_form

# HTML Pages
def home(request):
    return render(request, 'home/home.html')

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
        messages.success(request, "Your message has been successfully sent")

    context['form'] = form
    return render(request, 'home/createpost.html', context) 

# Authentication APIs
def handlesignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
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
            form1.save()
            obj = form.save(commit=False)
            obj.user = form1.save()
            obj.save()
            messages.success(request, "Your account has been successfully created")
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

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials: Please try again")
            return redirect('home')
    return HttpResponse('404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')



