from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Author, Post, Block, TextBlock, HighlightBlock, IndexConfiguration


def index(request):
    config = IndexConfiguration.get_solo()
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
        'featured_post': config.featured_post
    }
    return render(request, 'posts/index.html', context)


def post(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    rendered_blocks = []
    for block in post_obj.block_set.all():
        template = get_block_template(block)
        rendered_blocks.append(template.render({'block': block}))
    return render(request, 'posts/post/post.html',
                  {
                      'post': post_obj,
                      'blocks': rendered_blocks,
                  })


def author(request, author_id):
    author_obj = get_object_or_404(Author, pk=author_id)
    return render(request, 'posts/author.html', {'author': author_obj})


def get_block_template(block: Block):
    if isinstance(block, TextBlock):
        return loader.get_template('posts/post/blocks/text.html')
    if isinstance(block, HighlightBlock):
        return loader.get_template('posts/post/blocks/highlight.html')
    raise ValueError('Unexpected block class: ' + type(block).__name__)
