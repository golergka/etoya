from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def index(request):
    post_list = Post.objects.all()
    output = ', '.join([p.title for p in post_list])
    return HttpResponse("Posts: " + output)
