from django.shortcuts import render
from django.http import Http404

from .models import Post


def index(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    try:
        post_obj = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'posts/post.html', {'post': post_obj})

