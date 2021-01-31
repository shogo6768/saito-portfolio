from django.contrib.auth import get_user_model
from django.test import TestCase
from blogs.models import Category
import blogs.models
from accounts.models import CustomUser, Like, History

# Create your tests here

class TestCustomUser(TestCase):
    # カスタムユーザーのテスト
    @classmethod
    def setUpTestData(cls):
        # テスト用のユーザーを作成
        cls.user = CustomUser.objects.create(
            username='user', password='pass', email='email@gmail.com')

    def test_user_field_is_correct(self):
        # テストユーザーに正しく格納されているか、管理画面の表示名が正しいか検証
        user = CustomUser.objects.get(pk=1)
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.password, 'pass')
        self.assertEqual(user.email, 'email@gmail.com')
        self.assertEqual(str(user), user.username)


class TestLike(TestCase):
    # ライクモデルのテスト
    @classmethod
    def setUpTestData(cls):
        # テスト用のヒストリーを作成
        cls.user = CustomUser.objects.create(
            username='user', password='pass', email='email@gmail.com')
        cls.category = Category.objects.create(name='category', slug='cat')
        cls.post = blogs.models.PostModel.objects.create(
            title='post', category=cls.category)
        cls.like = Like.objects.create(user=cls.user, post=cls.post)

    def test_like_field_is_correct(self):
        # テストヒストリーに正しく格納されているか、管理画面の表示名が正しいか検証
        like = Like.objects.get(pk=1)
        self.assertEqual(like.user.username, 'user')
        self.assertEqual(like.post.title, 'post')
        self.assertEqual(str(like), like.created_at.strftime(
            '%Y/%m/%d %H:%M:%S')+'　'+'user'+'　'+'post')


class TestHistory(TestCase):
    # ヒストリーモデルのテスト
    @classmethod
    def setUpTestData(cls):
        # テスト用のヒストリーを作成
        cls.user = CustomUser.objects.create(
            username='user', password='pass', email='email@gmail.com')
        cls.category = Category.objects.create(name='category', slug='cat')
        cls.post = blogs.models.PostModel.objects.create(
            title='post', category=cls.category)
        cls.history = History.objects.create(user=cls.user, post=cls.post)

    def test_history_field_is_correct(self):
        # テストヒストリーに正しく格納されているか、管理画面の表示名が正しいか検証
        history = History.objects.get(pk=1)
        self.assertEqual(history.user.username, 'user')
        self.assertEqual(history.post.title, 'post')
        self.assertEqual(str(history), history.created_at.strftime(
            '%Y/%m/%d %H:%M:%S')+'　'+'user'+'　'+'post')
