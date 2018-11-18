from django.db import models
from polymorphic.models import PolymorphicModel


class Post(models.Model):
    """A single post, main feature of the site"""
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Block(PolymorphicModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('post', 'order',)
        ordering = ('order',)

    @classmethod
    def create(cls, post: Post):
        existing_blocks = post.block_set
        last_block = existing_blocks.order_by('order').last()
        next_order = last_block.order + 1 if last_block else 0
        return cls(post=post, order=next_order)


class TextBlock(Block):
    text = models.TextField()


class HighlightBlock(Block):
    text = models.TextField(max_length=1000)
