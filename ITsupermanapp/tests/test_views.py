from django.test import TestCase, RequestFactory
from ITsupermanapp.models import PostModel, Category
from ITsupermanapp.views import PostDetail, TopPage
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

class PostModelTestCase(TestCase):
    # def create_post(self, title, is_public):
    #     category = Category.objects.create(name='slack', slug='slack')
    #     return PostModel.objects.create(title=title, category=category)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(
            username='saito',
            email='aaakakaal@gmail.com',
            password='passabcd'
        )
        category = Category.objects.create(name='slack', slug='slack')
        self.obj1 = PostModel.objects.create(title="詳細ページのテスト", category=category, is_public='True' )
        self.obj2 = PostModel.objects.create(title="詳細ページのテスト", category=category, is_public='False' )
       
    def test_PostDetail_view(self):
        post_detail_url1 = reverse('post_detail', kwargs={'pk':self.obj1.pk})
        post_detail_url2 = reverse('post_detail', kwargs={'pk':self.obj2.pk})
        response1 = self.client.get(post_detail_url1)
        response2 = self.client.get(post_detail_url2)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)
    
    def test_PostDetail_context_auth(self):
        post_detail_url1 = reverse('post_detail', kwargs={'pk':self.obj1.pk})
        request = self.factory.get(post_detail_url1)
        request.user=self.user
        response= PostDetail.as_view()(request, pk=self.obj1.pk)
        self.assertIsNotNone(response.context_data['like'])
    
    def test_TopPage_view(self):
        toppage_url = reverse('toppage')
        response = self.client.get(toppage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toppage.html')

    def test_TopPage_view_auth(self):
        toppage_url = reverse('toppage')
        request = self.factory.get(toppage_url)
        request.user = self.user
        response = TopPage.as_view()(request)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)