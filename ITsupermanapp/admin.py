from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import Category, Tag, PostModel, CustomUser, Like, History, QuestionModel, AnswerModel, RequestModel

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostModel)
admin.site.register(CustomUser)
admin.site.register(Like)
admin.site.register(History)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
admin.site.register(RequestModel)
