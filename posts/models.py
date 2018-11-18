from django.db import models
from polymorphic.models import PolymorphicModel


class Post(models.Model):
    """A single post, main feature of the site"""
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Block(PolymorphicModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class TextBlock(Block):
    text = models.TextField()


class HighlightBlock(Block):
    text = models.TextField(max_length=1000)
