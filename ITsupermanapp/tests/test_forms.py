from django.test import TestCase
from ITsupermanapp.forms import ContactForm, QuestionForm
from ITsupermanapp.models import Category, PostModel

# Create your tests here
class ContactFormTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='slack', slug='slack')
        self.obj= PostModel.objects.create(title='A New title', category=category)

    def test_valid_form(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = 'form valid testです。'
        data = {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        contact_email = 'aaaaaaa@gmail.com'
        contact_subject ='テスト'
        contact_message = ''
        data = {'contact_email':contact_email, 'contact_subject':contact_subject, 'contact_message':contact_message}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())

# class QuestionFormTestCase(TestCase):
#     def test_valid_form(self):
#         title = 'excelの関数'
#         tags = '関数'
#         category = self.obj.category
#         content = '関数難しい'
#         data = {'title':title, 'category':category, 'tags':tags, 'content':content}
#         form = QuestionForm(data=data)
#         self.assertTrue(form.is_valid())