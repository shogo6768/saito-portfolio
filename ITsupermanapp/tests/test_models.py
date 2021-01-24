from django.test import TestCase
from ITsupermanapp.models import PostModel, Category


# Create your tests here
class PostModelTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='slack', slug='slack')
        PostModel.objects.create(title='A New title', category=category)
    
    def test_post_title(self):
        obj = PostModel.objects.get(pk=1)
        self.assertEqual(obj.title, 'A New title')
        self.assertTrue(obj.content == None)
        self.assertEqual(str(obj), obj.title)
    
    