from django.test import TestCase
from django.test import Client

from .models import Author, Post, HighlightBlock, TextBlock, IndexConfiguration


class AppTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Default author')
        self.author.save()

    def tearDown(self):
        if self.author:
            self.author.delete()


class PostBaseTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            title="Test title", author=self.author, lead="Test lead")
        self.post.save()

    def tearDown(self):
        if self.post:
            self.post.delete()
        super().tearDown()


class PostCreateTestCase(PostBaseTestCase):
    def test_post_exists(self):
        self.assertIsNotNone(self.post)

    def test_post_has_correct_title(self):
        self.assertEqual(self.post.title, "Test title")

    def test_post_has_correct_lead(self):
        self.assertEqual(self.post.lead, "Test lead")


class SingleBlockTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        self.block = TextBlock.create(post=self.post)
        self.block.text = "Text block"
        self.block.save()

    def tearDown(self):
        self.block.delete()
        super().tearDown()

    def test_post_contains_blocks(self):
        blocks = self.post.block_set.all()
        self.assertEqual(len(blocks), 1, 'post has 1 block')
        retrieved_block = blocks[0]
        self.assertIsNotNone(retrieved_block, 'block exists')
        self.assertIsInstance(retrieved_block, TextBlock, 'block is TextBlock')
        self.assertEqual(retrieved_block.text, "Text block",
                         'block has the right text')


class MultipleBlockTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        self.first_block = TextBlock.create(self.post)
        self.first_block.text = "First block"
        self.first_block.save()
        self.second_block = HighlightBlock.create(self.post)
        self.second_block.text = "Second block"
        self.second_block.save()

    def tearDown(self):
        self.first_block.delete()
        self.second_block.delete()

    def test_block_order(self):
        self.assertEqual(self.first_block.order, 0, 'first block order is 0')
        self.assertEqual(self.second_block.order, 1, 'second block order is 1')

    def test_post_block_set_length(self):
        blocks = self.post.block_set.all()
        self.assertEqual(len(blocks), 2, 'post has two blocks')

    def test_block_change_order(self):
        blocks = self.post.block_set
        self.assertEqual(blocks.all()[0].text, "First block",
                         'first block in first place before changing order')
        self.assertEqual(blocks.all()[1].text, "Second block",
                         'second block in second place before changing order')

        self.first_block.order = 2
        self.first_block.save()

        self.assertEqual(blocks.all()[0].text, "Second block",
                         'second block in first place after changing order')
        self.assertEqual(blocks.all()[1].text, "First block",
                         'second block in second place after changing order')


class IndexViewPostsTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.first_post = Post.objects.create(
            title="First post", author=self.author)
        self.second_post = Post.objects.create(
            title="Second post", author=self.author)

    def tearDown(self):
        self.first_post.delete()
        self.second_post.delete()
        super().tearDown()

    def test_correct_post_list(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'Response status code 200')

        post_list = response.context['post_list']
        self.assertIsNotNone(post_list, 'post_list exists')
        self.assertEqual(len(post_list), 2, 'post_list has 2 posts')
        self.assertEqual(post_list[0].title, 'First post',
                         'post_list post 1 has correct title')
        self.assertEqual(post_list[1].title, 'Second post',
                         'post_list post 2 has correct title')


class IndexViewWithoutFeaturedTestCase(AppTestCase):
    def test_featured_post_is_none(self):
        client = Client()
        response = client.get('/')

        self.assertIsNone(
            response.context['featured_post'], 'Context does not have featured post')


class IndexViewWithFeaturedPostTestCase(PostBaseTestCase):
    def setUp(self):
        super().setUp()
        index_config = IndexConfiguration.get_solo()
        index_config.featured_post = self.post
        index_config.save()

    def tearDown(self):
        index_config = IndexConfiguration.get_solo()
        index_config.featured_post = None
        index_config.save()
        super().tearDown()

    def test_featured_post_exists(self):
        client = Client()

        response = client.get('/')

        self.assertIsNotNone(
            response.context['featured_post'], 'Context has featured post')
        self.assertEqual(
            response.context['featured_post'].title, 'Test title', 'Context has correct featured post')


class PostViewTestCase(PostBaseTestCase):
    client = Client()

    def setUp(self):
        super().setUp()
        self.text_block = TextBlock.create(self.post)
        self.text_block.text = "Text block"
        self.text_block.save()
        self.highlight_block = HighlightBlock.create(self.post)
        self.highlight_block.text = "Highlight block"
        self.highlight_block.save()
        self.response = self.client.get('/' + str(self.post.pk) + '/')

    def tearDown(self):
        self.text_block.delete()
        self.highlight_block.delete()
        super().tearDown()

    def test_response_status(self):
        self.assertEqual(self.response.status_code, 200,
                         'Existing post view code 200')

    def test_response_details(self):
        loaded_post = self.response.context['post']
        self.assertIsNotNone(loaded_post, 'post exists')
        self.assertEqual(loaded_post.title, "Test title",
                         "post has correct title")

    def test_response_blocks(self):
        blocks = self.response.context['blocks']
        self.assertEqual(len(blocks), 2, 'Post has two blocks')
