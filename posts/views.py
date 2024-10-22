from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.all()

    context = {'posts': posts}

    return render(
        request, 
        'blog/post/list.html',
        context
    )


def post_details(request, uuid):
    post = get_object_or_404(Post, uuid=uuid, status=Post.Status.PUBLISHED)
    
    context = {'post': post}

    return render(
        request,
        'blog/post/detail.html',
        context
    )
