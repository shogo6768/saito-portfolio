from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children' ,on_delete=models.CASCADE, blank=True, null=True)
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

# 12/19 斉藤コメント　ユーザーモデル拡張タイプに戻しました。
class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    email = models.CharField(verbose_name='メールアドレス', max_length=50)
    password = models.CharField(verbose_name='パスワード', max_length=30)
    history = models.PositiveIntegerField(verbose_name='history', default=0)
     # お気に入り機能格納用のフィールド追加
    like_post = models.ManyToManyField(
        PostModel, verbose_name='like', blank=True)

    def __str__(self):
        return self.username
