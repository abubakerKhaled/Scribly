from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Post
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag

def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

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

    context = {
        'posts': posts,
        'tag': tag,
        }

    return render(
        request, 
        'posts/post/list.html',
        context
    )


class PostListView(ListView):
    """
    Post List View
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'


def post_detail(request, uuid):
    post = get_object_or_404(Post, uuid=uuid, status=Post.Status.PUBLISHED)
    recent_posts = Post.objects.exclude(uuid=post.uuid).order_by("-created")[:5]
    posts = Post.objects.all()  # Add this line

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    context = {
        'posts': posts,
        "post": post,
        "recent_posts": recent_posts,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }

    return render(
        request,
        'posts/post/detail.html',
        context
    )

def post_share(request, post_uuid):
    # Retrieve post by id
    post = get_object_or_404(
        Post, 
        uuid=post_uuid,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
        
    else:
        form = EmailPostForm()

    context = {
        'form': form,
        'post': post,
        'sent': sent,
    }
    return render(
        request,
        'posts/post/share.html',
        context
    )

@require_POST
def post_comment(request, post_uuid):
    post = get_object_or_404(Post, uuid=post_uuid, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save teh comment to the database
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(
        request,
        "posts/post/comment.html",
        context,
    )


def post_search(request):
    form = SearchForm(request.GET)
    query = None
    if form.is_valid():
        query = form.cleaned_data["query"]
        results = Post.published.annotate(
            search=SearchVector("title", "body"),
        ).filter(search=query)
    else:
        results = []

    return render(
        request,
        "posts/post/search.html",
        {"form": form, "query": query, "results": results},
    )
