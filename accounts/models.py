from django.db import models
from django.contrib.auth.models import AbstractUser


# 1/14　ユーザーモデル内のlike, historyはLike、Historyモデルに切り出し
class CustomUser(AbstractUser):
    email = models.CharField(verbose_name='メールアドレス', max_length=50)
    password = models.CharField(verbose_name='パスワード', max_length=30)

    def __str__(self):
        return self.username

class Like(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='user', blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'blogs.PostModel', verbose_name='post', blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.created_at.strftime('%Y/%m/%d %H:%M:%S')+'　'+self.user.username+'　'+self.post.title


class History(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='user', blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'blogs.PostModel', verbose_name='post', blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.created_at.strftime('%Y/%m/%d %H:%M:%S')+'　'+self.user.username+'　'+self.post.title


