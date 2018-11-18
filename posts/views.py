from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Post


def index(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post.html', {'post': post_obj})

