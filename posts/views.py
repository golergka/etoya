from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Post


def index(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }
    return render(request, 'posts/index.html', context)
