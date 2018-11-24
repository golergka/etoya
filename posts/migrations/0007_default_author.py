# Generated by Django 2.1.3 on 2018-11-24 03:53

from django.db import migrations


def create_default_author(apps, _):
    author_cls = apps.get_model('posts', 'Author')
    post_cls = apps.get_model('posts', 'Post')
    default_author = author_cls.objects.create(name='Default author')
    default_author.save()
    for post in post_cls.objects.all():
        post.author = default_author
        post.save()


def delete_default_author(apps, _):
    post_cls = apps.get_model('posts', 'Post')
    for post in post_cls.objects.all():
        if post.author:
            post.author.delete()
            post.author = None
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20181124_0351'),
    ]

    operations = [
        migrations.RunPython(create_default_author, delete_default_author),
    ]
