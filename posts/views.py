from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.all()

    context = {'posts': posts}

    return render(
        request, 
        'posts/post/list.html',
        context
    )


def post_detail(request, uuid):
    post = get_object_or_404(Post, uuid=uuid, status=Post.Status.PUBLISHED)
    
    context = {'post': post}

    return render(
        request,
        'posts/post/detail.html',
        context
    )
