from django.test import TestCase, RequestFactory, Client
from blogs.models import Category
from QA.models import QuestionModel, AnswerModel
from accounts.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from QA.forms import QuestionForm
from django.core.mail import BadHeaderError
from django.utils import timezone



class QuestionTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            # create →create_user
            username='admin',
            email='saitou@gmail.com',
            password='pass'
        )
        self.user2 = get_user_model().objects.create_user(
            # create →create_user
            username='saito',
            email='1234567@gmail.com',
            password='pass'
        )
        self.category = Category.objects.create(name='slack', slug='slack')
        self.question = QuestionModel.objects.create(
            title='エクセルわからない',
            category=self.category,
            tags='aaa',
            content='hahahahaa',
            created_by=self.user,
        )
        # self.client = Client()
        self.question_create_url = reverse('question_form')
        self.question_list_url = reverse('question_list')
        self.question_update_url = reverse('question_update', kwargs={'pk':self.question.pk})
        self.question_delete_url = reverse('question_delete', kwargs={'pk':self.question.pk})

    def test_QuestionCreate_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_create_url)
        self.assertEqual(response.status_code, 200)

    def test_QuestionCreate_post(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        data={
            'title' : 'テスト',
            'category' : self.category,
            'tags' : 'aaa', 
            'content' : '',
            'created_by': self.user
            # 'created_at':timezone.now(),
            # 'updated_at':timezone.now(),
        }
        form = QuestionForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post( self.question_create_url , data)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, '/question_list/')
    

    def test_QuestionCreate_valid_form(self):
        
        title='テスト'
        category=self.category
        tags='aaa'
        content='hahahahaa'
        data = {'title':title, 'category':category, 'tags':tags, 'content':content}
        form = QuestionForm(data=data)
        self.assertTrue(form.is_valid())

        # request = self.factory.post(self.question_create_url, {'form':form})
        # request.user = self.user
        # form.instance.created_by=request.user
        # response = QuestionCreate.as_view()(request)
        # self.assertEqual(response.status_code, 302)
 
    def test_QuestionList_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, 200)

    def test_QuestionUpdate_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_update_url)
        self.assertEqual(response.status_code, 200)
        
    def test_QuestionUpdate_access_limit(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.get(self.question_update_url)
        self.assertEqual(response.status_code, 302)
    
    def test_QuestionUpdate_post(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        # data={
        #     'title':'変更します',
        #     'category':self.question.category,
        #     'tags':self.question.tags,
        #     'content': 'self.question.content',
        # }
        response = self.client.post(self.question_update_url, {'title':'変更します'})
        self.assertEqual(response.status_code, 200)

    def test_QuestionDelete_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_delete_url)
        self.assertEqual(response.status_code, 200)
    
    def test_QuestionDelete_access_limit(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.get(self.question_delete_url)
        self.assertEqual(response.status_code, 302)
    
    def test_QuestionDelete_delete(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.delete(self.question_delete_url)
        self.assertEqual(response.status_code, 302)

class QuestionAnswerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            # create →create_user
            username='admin',
            email='saitou@gmail.com',
            password='pass'
        )
        self.user2 = get_user_model().objects.create_user(
            # create →create_user
            username='saito',
            email='1234567@gmail.com',
            password='pass'
        )
        self.client = Client()
        self.category = Category.objects.create(name='slack', slug='slack')
        self.question = QuestionModel.objects.create(
            title='テスト',
            category=self.category,
            tags='aaa',
            content='hahahahaa',
            created_by=self.user,
        )
        self.answer = AnswerModel.objects.create(
            question=self.question,
            answer='テスト',
            created_by=self.user2,
        )
        self.question_answer_url = reverse('question_answer', kwargs={'pk':self.question.pk})
        self.question_request_url = reverse('question_request', kwargs={'pk':self.question.pk})
        self.answer_update_url = reverse('answer_update', kwargs={'pk':self.question.pk, 'answer_pk':self.answer.pk})
        self.answer_delete_url = reverse('answer_delete', kwargs={'pk':self.question.pk, 'answer_pk':self.answer.pk})
        


    def test_questionAnswer_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_answer_url)
        self.assertEqual(response.status_code, 200)
    
    def test_questionAnswer_post(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.post(self.question_answer_url, {'answer':'aaaaaaa'})
        self.assertEqual(response.status_code, 302)
    
    def test_questionRequest_get(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.question_request_url)
        self.assertEqual(response.status_code, 200)

    def test_questionRequest_Post(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        subject = 'テスト'
        message ='嗚呼あ'
        response = self.client.post(self.question_request_url, {'subject':subject, 'message':message, 'pk':self.question.pk})
        self.assertEqual(response.status_code, 302)
    
    def test_questionRequest_post_headererror(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        subject = 'Subject\nInjection Test'
        message ='嗚呼嗚呼'
        response = self.client.post(self.question_request_url, {'subject':subject, 'message':message, 'pk':self.question.pk})
        self.assertRaises(BadHeaderError)

    def test_questionRequest_post_form_invalid(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        subject =''
        message = ''
        response = self.client.post(self.question_request_url, {'subject':subject, 'message':message, 'pk':self.question.pk})
        self.assertEqual(response.status_code, 200)

    def test_AnswerUpdate_get(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.get(self.answer_update_url)
        self.assertEqual(response.status_code, 200)
        
    def test_AnswerUpdate_access_limit(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.answer_update_url)
        self.assertEqual(response.status_code, 302)
    
    def test_AnswerUpdate_post(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.post(self.answer_update_url, {'answer':'回答調整'})
        self.assertEqual(response.status_code, 302)
    
    def test_AnswerDelete_get(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.get(self.answer_delete_url)
        self.assertEqual(response.status_code, 200)
    
    def test_AnswerDelete_access_limit(self):
        logged_in =self.client.login(username=self.user.username, password='pass')
        response = self.client.get(self.answer_delete_url)
        self.assertEqual(response.status_code, 302)
    
    def test_AnswerDelete_delete(self):
        logged_in =self.client.login(username=self.user2.username, password='pass')
        response = self.client.delete(self.answer_delete_url)
        self.assertEqual(response.status_code, 302)



        
    