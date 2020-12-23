from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import Category, Tag, PostModel, CustomUser

# 管理画面のManyToManyフィールドカスタマイズ
class CustomUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('like_post',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostModel)
admin.site.register(CustomUser, CustomUserAdmin)
