from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import BlogPost


def index(request):
    posts = BlogPost.objects.filter(is_published=True).select_related('author')
    return render(request, 'newsroom/index.html', {
        'posts': posts,
        'page_title': 'Newsroom',
    })


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'newsroom/post.html', {
        'post': post,
        'page_title': post.title,
    })
