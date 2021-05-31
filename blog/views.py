from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from blog.models import Post, BlogComment, postviews, usercount
from django.contrib import messages
from blog.templatetags import extras
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def bloghome(request):
    allposts = Post.objects.all()
    posts   = Post.objects.filter().order_by('-views')[:3]

    #pagination
    paginator = Paginator(allposts, 2)
    page = request.GET.get('page')
    try:
        allposts = paginator.page(page)
    except PageNotAnInteger:
        allposts = paginator.page(1)
    except EmptyPage:
        allposts = paginator.page(paginator.num_pages)

    context = {'allposts': allposts, 'user':str(request.user), 'page':page, 'posts': posts}
    return render(request, 'blog/bloghome.html', context)


def blogpost(request, slug):
    post     = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies  = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    for reply in replies:
        if reply.parent.Sno not in replyDict.keys():
            replyDict[reply.parent.Sno] = [reply]
        else:
            replyDict[reply.parent.Sno].append(reply)

    # for authenticate user
    user = request.user
    author = post.author
    abc = str(request.user)
    view = postviews.objects.filter(post=post).first()
    
    if user.is_authenticated:
        username = user.first_name + " " + post.title
        if postviews.objects.filter(post=post).exists():         
            if usercount.objects.filter(user=username).exists():
                pass
            else:
                createuser = usercount(user=username)
                createuser.save()
                count = view.views + 1
                postviews.objects.filter(post=post).update(views=count)
        else:
            createuser = usercount(user=username)
            createuser.save()
            view = postviews(post=post, views=1)
            view.save()

    # for anonymous user
    else:
        def get_ip(request):
            adress = request.META.get('HTTP_X_FORWARDED_FOR')
            if adress:
                ip = adress.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            return ip   

        ip = get_ip(request)
        
        result = postviews.objects.filter(Q(user__icontains=ip))
        
        if postviews.objects.filter(post=post).exists():
            username = ip + " " + post.title
            if usercount.objects.filter(user=username).exists():
                pass
            else:
                createuser = usercount(user=username)
                createuser.save()
                view = postviews.objects.filter(post=post).first()
                count = view.views + 1
                postviews.objects.filter(post=post).update(views=count)

        else:
            username = ip + " " + post.title
            createuser = usercount(user=username)
            createuser.save()
            view = postviews(post=post, views=1)
    counts = view.views
    post.views = counts
    post.save()

    
    context  = {'post': post, 'comments': comments, 'user': request.user, 'replyDict':replyDict, 'is_liked':is_liked, 'total_likes':post.total_likes(),'author':str(author), 'abc':abc}

    return render(request, 'blog/blogpost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(Sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(
                request, "Your comment has been posted successfully")    

        else:
            parent = BlogComment.objects.get(Sno=parentSno)
            comment = BlogComment(
                comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(
                request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")

def like_post(request):
    if request.method == "POST":
        post = get_object_or_404(Post, Sno=request.POST.get('postSno'))
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            messages.success(
                request, "You disliked this post")

        else:   
            post.likes.add(request.user)
            messages.success(
                request, "You liked this post")

    return redirect(f"/blog/{post.slug}")

def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == str(request.user):
        if request.method == 'POST':
            post.delete()
            messages.success(request, "You have successfully deleted your post")
            return redirect('bloghome')
    return redirect(f'/blog/{post.slug}')
