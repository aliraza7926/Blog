from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):
    
    def setUp(self):
        self.user=get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        
        self.post = Post.objects.create(
            title='This is a title',
            body='This is a body',
            author=self.user,
        )

    def test_string_representation(self):
        post=Post(title='Title')
        self.assertEqual(str(post),post.title)
    
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}','This is a title')
        self.assertEqual(f'{self.post.author}','testuser')
        self.assertEqual(f'{self.post.body}','This is a body')

    def test_post_list_view(self):
        response=self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'This is a body')
        self.assertTemplateUsed(response,'home.html')

    def test_post_detail_view(self):
        response=self.client.get('/post/1/')
        no_response=self.client.get('/post/1000/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response,'This is a title')
        self.assertTemplateUsed(response,'post_detail.html')