from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import PostList, PostDetail, PostLike, about, search


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, PostList)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search)

    def test_detail_url_resolves(self):
        url = reverse('post_detail', args=['test-slug'])
        self.assertEqual(resolve(url).func.view_class, PostDetail)

    def test_like_url_resolves(self):
        url = reverse('post_like', args=['test-slug'])
        self.assertEqual(resolve(url).func.view_class, PostLike)
