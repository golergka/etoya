from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment, teardown_test_environment

from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Test title")

    def test_correct_title(self):
        test_post = Post.objects.get(title="Test title")
        self.assertIsNotNone(test_post, 'Test post exists')

class IndexViewTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post1")
        Post.objects.create(title="Post2")

    def test_correct_post_list(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'Response status code 200')

        post_list = response.context['post_list']
        self.assertIsNotNone(post_list, 'post_list exists')
        self.assertEqual(len(post_list), 2, 'post_list has 2 posts')
        self.assertEqual(post_list[0].title, 'Post1', 'post_list post 1 has correct title')
        self.assertEqual(post_list[1].title, 'Post2', 'post_list post 2 has correct title')

