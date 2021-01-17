from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PostModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    # アイキャッチ画像のフィールド追加（$pip install pillowが必要）
    eye_catch = models.ImageField(upload_to='media/', blank=True)
    content = RichTextUploadingField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


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
        PostModel, verbose_name='post', blank=True, on_delete=models.CASCADE)
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
        PostModel, verbose_name='post', blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.created_at.strftime('%Y/%m/%d %H:%M:%S')+'　'+self.user.username+'　'+self.post.title


class QuestionModel(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class AnswerModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name='answers')
    answer = RichTextUploadingField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name='requests')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
