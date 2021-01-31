from django.test import TestCase, RequestFactory, Client
from django import forms
from blogs.models import PostModel, Category
from accounts.models import CustomUser, Like, History
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.core.mail import BadHeaderError
from django.utils import timezone


class TestCreateUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', email='test@example.com', password='pass')

    def test_get_success(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'accounts/create.html')

    def test_get_by_unauthenticated_user(self):
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('create'))
        self.assertRedirects(response,
                             reverse('mypage', kwargs={"pk": self.user.pk}))

    def test_post_success(self):
        self.assertFalse(get_user_model().objects.filter(
            username='test_user').exists())
        response = self.client.post(reverse('create'), {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'pass',
            'password2': 'pass'
        })
        self.assertRedirects(response, reverse(
            'mypage', kwargs={"pk": get_user_model().objects.get(username='test_user').pk}))
        self.assertTrue(get_user_model().objects.filter(
            username='test_user').exists())

    def test_post_unique_constraint(self):
        self.assertTrue(get_user_model().objects.filter(
            username='user').exists())
        response = self.client.post(reverse('create'), {
            'username': self.user.username,
            'email': self.user.email,
            'password': 'pass',
            'password2': 'pass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', '同じユーザー名が既に登録済みです。')
        self.assertTemplateUsed(response, 'accounts/create.html')

    def test_post_name_too_short(self):
        response = self.client.post(reverse('create'), {
            'username': 'a',
            'email': 'email@email.com',
            'password': 'pass',
            'password2': 'pass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', '3文字以上で入力してください')
        self.assertTemplateUsed(response, 'accounts/create.html')

    def test_post_pass12_not_match(self):
        response = self.client.post(reverse('create'), {
            'username': 'test',
            'email': 'email@email.com',
            'password': 'pass1',
            'password2': 'pass2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None,
                             'パスワードと確認用パスワードが合致しません')
        self.assertTemplateUsed(response, 'accounts/create.html')


class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', email='test@example.com', password='pass')

    def test_get_success(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].errors)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_post_success(self):
        logged_in = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'pass'
        })
        self.assertTrue(logged_in)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response,
                             reverse('mypage', kwargs={"pk": self.user.pk}))

    def test_post_unique_constraint(self):
        response = self.client.post(reverse('login'), {
            'username': 'dummy',
            'password': 'pass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, "正しいユーザー名を入力してください")
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_post_name_too_short(self):
        response = self.client.post(reverse('login'), {
            'username': 'a',
            'password': 'pass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', '3文字以上で入力してください')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_post_pass_not_match(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'dummy_pass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, '正しいユーザー名とパスワードを入力してください')
        self.assertTemplateUsed(response, 'accounts/login.html')


class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', password='pass', email='test@example.com')

    def test_get_success(self):
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('toppage'))
        re_login_response = self.client.get(reverse('login'))
        self.assertTemplateUsed(re_login_response, 'accounts/login.html')

    def test_get_in_unauthenticated(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('toppage'))


class TestResignView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', password='pass', email='test@example.com')

    def test_get_success(self):
        self.assertTrue(get_user_model().objects.filter(
            username='user').exists())
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('resign'))
        self.assertEqual(response.status_code, 200)
        response_cnd = self.client.get(
            reverse('resign_conduct', kwargs={"pk": self.user.pk}))
        self.assertFalse(get_user_model().objects.filter(
            username='user').exists())
        self.assertEqual(response_cnd.status_code, 302)
        self.assertRedirects(response_cnd, reverse('resign_complete'))

    def test_get_by_unauthenticated_user(self):
        response = self.client.get(reverse('resign'))
        self.assertRedirects(response, reverse('login')+'?next=/accounts/resign/')
        response_cnd = self.client.get(
            reverse('resign_conduct', kwargs={"pk": self.user.pk}))
        self.assertRedirects(response_cnd, reverse(
            'login') + '?next=' + reverse('resign_conduct', kwargs={"pk": self.user.pk}))
        response_cmp = self.client.get(reverse('resign_complete'))
        self.assertTemplateUsed(response_cmp, 'accounts/resign_complete.html')


class TestMyPageView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', password='pass', email='test@example.com')
        cls.category = Category.objects.create(name='name', slug='slug')
        cls.post = PostModel.objects.create(
            title="title", category=cls.category, is_public='True')

    def test_get_success(self):
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse('save_history', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        history = History.objects.get(
            user=self.user, post=self.post)
        self.assertEqual(history.post.category, self.post.category)
        response = self.client.get(
            reverse('mypage', kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/mypage.html')

    def test_get_by_unauthenticated_user(self):
        response = self.client.get(
            reverse('mypage', kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'login') + '?next=' + reverse('mypage', kwargs={"pk": self.user.pk}))


class TestSaveHistory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', password='pass', email='test@example.com')
        cls.category = Category.objects.create(name='name', slug='slug')
        cls.post = PostModel.objects.create(
            title="title", category=cls.category, is_public='True')

    def test_get_by_authenticated(self):
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse('save_history', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        self.assertTrue(History.objects.filter(
            user=self.user, post=self.post).exists())

    def test_get_by_unauthenticated(self):
        response = self.client.get(
            reverse('save_history', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        self.assertFalse(History.objects.filter(
            user=self.user, post=self.post).exists())

    def test_in_exist_case(self):
        history = History.objects.create(user=self.user, post=self.post)
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse('save_history', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        self.assertTrue(History.objects.filter(
            user=self.user, post=self.post).exists())


class TestLike(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', password='pass', email='test@example.com')
        cls.category = Category.objects.create(name='name', slug='slug')
        cls.post = PostModel.objects.create(
            title="title", category=cls.category, is_public='True')

    def test_get_by_authenticated(self):
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse('like', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        self.assertTrue(Like.objects.filter(
            user=self.user, post=self.post).exists())

    def test_get_by_unauthenticated(self):
        response = self.client.get(
            reverse('like', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'login') + '?next=' + reverse('like', kwargs={"pk": self.post.pk}))
        self.assertFalse(Like.objects.filter(
            user=self.user, post=self.post).exists())

    def test_in_exist_case(self):
        like = Like.objects.create(user=self.user, post=self.post)
        logged_in = self.client.login(username='user', password='pass')
        self.assertTrue(logged_in)
        response = self.client.get(
            reverse('like', kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse(
            'post_detail', kwargs={"pk": self.post.pk}))
        self.assertFalse(Like.objects.filter(
            user=self.user, post=self.post).exists())

        
    