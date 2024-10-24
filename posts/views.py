from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    post_list = Post.published.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer get teh first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}

    return render(
        request, 
        'posts/post/list.html',
        context
    )


def post_detail(request, uuid):
    post = get_object_or_404(Post, uuid=uuid, status=Post.Status.PUBLISHED)
    recent_posts = Post.objects.exclude(uuid=post.uuid).order_by("-created")[:5]
    posts = Post.objects.all()  # Add this line
    context = {
        'posts': posts,
        "post": post,
        "recent_posts": recent_posts,
    }

    return render(
        request,
        'posts/post/detail.html',
        context
    )
