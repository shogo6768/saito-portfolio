from django.test import TestCase
from QA.models import QuestionModel
from blogs.models import Category
from accounts.models import CustomUser

# Create your tests here    
class QuestionModelTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='slack', slug='slack')
        created_by = CustomUser.objects.create(
            username='saito',
            email='aaakakaal@gmail.com',
            password='passabcd'
        )
        self.obj=QuestionModel.objects.create(title='A New title', category=category, tags='タグ', content='テストです。', created_by=created_by)
    
    def test_question_model(self):
        self.assertEqual(str(self.obj), self.obj.title)