from django.test import TestCase
from QA.forms import  QuestionForm, RequestForm
from blogs.models import Category

# Create your tests here

class QuestionFormTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='slack', slug='slack')

    def test_valid_form(self):
        title = 'excelの関数'
        tags = '関数'
        category = self.category
        content = '関数難しい'
        data = {'title':title, 'category':category, 'tags':tags, 'content':content}
        form = QuestionForm(data=data)
        self.assertTrue(form.is_valid())


class RequestFormTestCase(TestCase):
    def test_valid_form(self):
        subject = '詳細求'
        message = '情報が足りません'
        data = {'subject':subject, 'message':message}
        form = RequestForm(data=data)
        self.assertTrue(form.is_valid())