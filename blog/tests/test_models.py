from django.test import TestCase
from blog.models import Post, Comment
from django.contrib.auth.models import User


class TestModels(TestCase):

    def test_post_status_defaults_to_draft(self):
        user = User.objects.create(username='testname')
        post = Post.objects.create(
            title='post1',
            author=user
        )
        self.assertFalse(post.status)

    def test_comment_approved_defaults_to_false(self):
        user = User.objects.create(username='testname')
        post = Post.objects.create(
            title='post1',
            author=user
        )
        comment = Comment.objects.create(
            post=post,
            body='post comment',
        )
        self.assertFalse(comment.approved)

    def test_post_string_method_returns_title(self):
        user = User.objects.create(username='testname')
        post = Post.objects.create(
            title='post1',
            author=user
        )
        self.assertEqual(str(post), 'post1')

    def test_comment_string_method_returns_comment(self):
        user = User.objects.create(username='testname')
        post = Post.objects.create(
            title='post1',
            author=user
        )
        comment = Comment.objects.create(
            post=post,
            name=user,
            body='post comment',
        )
        self.assertEqual(str(comment), 'Comment post comment by testname')
