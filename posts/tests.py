from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment, teardown_test_environment

from .models import Post, Block, HighlightBlock, TextBlock, IndexConfiguration


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Test title")

    def test_correct_title(self):
        test_post = Post.objects.get(title="Test title")
        self.assertIsNotNone(test_post, 'Test post exists')


class BlockTests(TestCase):
    def test_post_contains_blocks(self):
        test_post = Post.objects.create(title="Test post title")
        test_post.save()
        text_block = TextBlock.create(post=test_post)
        text_block.text = "Text block"
        text_block.save()
        blocks = test_post.block_set.all()
        self.assertEqual(len(blocks), 1, 'test_post has 1 block')
        retrieved_block = blocks[0]
        self.assertIsNotNone(retrieved_block, 'block exists')
        self.assertIsInstance(retrieved_block, TextBlock, 'block is TextBlock')
        self.assertEqual(retrieved_block.text, "Text block",
                         'block has the right text')

    def test_block_order_unique(self):
        test_post = Post.objects.create(title="Test post title")
        test_post.save()

        text_block = TextBlock.create(test_post)
        text_block.save()
        highlight_block = HighlightBlock.create(test_post)
        highlight_block.save()

        self.assertEqual(text_block.order, 0, 'first block order is 0')
        self.assertEqual(highlight_block.order, 1, 'second block order is 1')

        blocks = test_post.block_set.all()
        self.assertEqual(len(blocks), 2, 'post has two blocks')

    def test_block_default_ordering(self):
        test_post = Post.objects.create(title="Test post title")
        test_post.save()
        block1 = TextBlock.create(test_post)
        block1.text = "Block1"
        block1.save()
        block2 = TextBlock.create(test_post)
        block2.text = "Block2"
        block2.save()

        self.assertEqual(test_post.block_set.all()[0].text, "Block1",
                         'first block in first place before changing order')
        self.assertEqual(test_post.block_set.all()[1].text, "Block2",
                         'second block in second place before changing order')

        block1.order = 2
        block1.save()

        self.assertEqual(test_post.block_set.all()[0].text, "Block2",
                         'second block in first place after changing order')
        self.assertEqual(test_post.block_set.all()[1].text, "Block1",
                         'second block in second place after changing order')


class IndexViewTests(TestCase):
    def test_correct_post_list(self):
        Post.objects.create(title="Post1")
        Post.objects.create(title="Post2")
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'Response status code 200')

        post_list = response.context['post_list']
        self.assertIsNotNone(post_list, 'post_list exists')
        self.assertEqual(len(post_list), 2, 'post_list has 2 posts')
        self.assertEqual(post_list[0].title, 'Post1',
                         'post_list post 1 has correct title')
        self.assertEqual(post_list[1].title, 'Post2',
                         'post_list post 2 has correct title')

    def test_featured_post_none(self):
        index_config = IndexConfiguration.get_solo()
        index_config.featured_post = None
        client = Client()

        response = client.get('/')

        self.assertIsNone(
            response.context['featured_post'], 'Context does not have featured post')

    def test_featured_post_exists(self):
        post = Post.objects.create(title="Featured post")
        post.save()
        index_config = IndexConfiguration.get_solo()
        index_config.featured_post = post
        index_config.save()
        client = Client()

        response = client.get('/')

        self.assertIsNotNone(
            response.context['featured_post'], 'Context has featured post')
        self.assertEqual(
            response.context['featured_post'].title, 'Featured post', 'Context has correct featured post')


class PostViewTests(TestCase):
    client = Client()

    def test_post_wrong_id(self):
        response = self.client.get('/234/')
        self.assertEqual(response.status_code, 404,
                         "Absent post status code 404")

    def test_post_simple(self):
        created_post = Post.objects.create(title="Test post title")
        response = self.client.get('/' + str(created_post.pk) + '/')
        self.assertEqual(response.status_code, 200,
                         'Existing post view code 200')

        loaded_post = response.context['post']
        self.assertIsNotNone(loaded_post, 'post exists')
        self.assertEqual(loaded_post.title, "Test post title",
                         "post has correct title")

    def test_blocks(self):
        post = Post.objects.create()
        post.save()
        text_block = TextBlock.create(post)
        text_block.text = "Text block"
        text_block.save()
        highlight_block = HighlightBlock.create(post)
        highlight_block.text = "Highlight block"
        highlight_block.save()

        response = self.client.get('/' + str(post.pk) + '/')
        blocks = response.context['blocks']
        self.assertEqual(len(blocks), 2, 'Post has two blocks')
