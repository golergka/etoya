from django.test import TestCase
from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Test title")

    def test_correct_title(self):
        test_post = Post.objects.get(title="Test title")
        self.assertIsNotNone(test_post, 'Test post exists')
