from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView
from .models import QuestionModel, AnswerModel, RequestModel
from accounts.models import CustomUser
from blogs.models import PostModel, Category
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
# メール送信のための追加インポート
from django.core.mail import send_mail, BadHeaderError
# 追加インポート
import logging
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.conf import settings
from django.contrib import messages
from itertools import chain
from django.core.exceptions import PermissionDenied
# フォーム定義
from .forms import QuestionForm, AnswerForm, RequestForm
from django import template
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionCreate(CreateView):
    template_name = 'questionForm.html'
    form_class = QuestionForm
    model = QuestionModel

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self,  **kwargs):
        return reverse('question_list', kwargs={"pk": 1})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context
    

# @login_required(login_url='/accounts/login/')
# def QuestionCreate(request):
#     allcats = Category.objects.filter(parent=None)
#     if request.method == 'GET':
#         form = QuestionForm()
#         return render(request, 'questionForm.html', {'form': form, 'allcats': allcats})
#     else:
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.created_by = request.user
#             # form.instance.created_by = request.user
#             question.save()
#             return redirect('question_list')    
#     return render(request, 'questionForm.html', {'form': form, 'allcats': allcats})


# @login_required(login_url='/accounts/login/')
# def QuestionList(request, pk):
#     allcats = Category.objects.filter(parent=None)
#     print(pk)
#     if  pk == 1:
#         questions = QuestionModel.objects.all()
#         return render(request, "questionList.html", {
#         'allcats':allcats,
#         'questions': questions,
#     })

#     elif pk == 2:
#         answers = AnswerModel.objects.all()
#         return render(request, "questionList.html", {
#         'answers':answers,
#         'allcats':allcats,
#     })

#     else:
#         answers =AnswerModel.objects.all().get(answer=not None)
#         question = answers.question
#         return render(request, "questionList.html", {
#         'allcats':allcats,
#         'questions': questions,
#     })

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionList(ListView):
    template_name = 'questionList.html'
    model = QuestionModel

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = QuestionModel.objects.all().order_by('-created_at')
        context["questions"] = question
        context["pk"] = self.kwargs['pk']
        context["allcats"] = Category.objects.filter(parent=None)
        return context

@login_required(login_url='/accounts/login/')
def questionAnswer(request, pk):
    allcats = Category.objects.filter(parent=None)
    # 質問文
    question = get_object_or_404(QuestionModel, pk=pk)
    question.views += 1
    question.save()
    # 回答文
    answers = question.answers.all()
    counts = answers.count()
    # 新規回答文
    new_comment = None
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.question = question
            new_answer.created_by = request.user
            new_answer.save()
            return redirect('question_answer', pk=question.pk)
    else:
        answer_form = AnswerForm()

    return render(request, "questionAnswer.html", {
        'allcats':allcats,
        'question': question,
        'answers': answers,
        'form': answer_form,
        'counts': counts
    })

# 1/10 編集request追加

@login_required(login_url='/accounts/login/')
def QuestionRequest(request, pk):
    # allcatsはheaderのためのcontext
    allcats = Category.objects.filter(parent=None)
    question = get_object_or_404(QuestionModel, pk=pk)
    if request.method == 'GET':
        form = RequestForm()
        return render(request, 'questionRequest.html', {'form': form, 'allcats': allcats, 'question': question})
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
            request_subject = form.cleaned_data['subject']
            request_message = form.cleaned_data['message']
            from_email = "no-reply@em9607.plusit-1.com"
            to_email = QuestionModel.objects.get(pk=pk).created_by.email
            try:
                send_mail(request_subject, request_message,
                          from_email, [to_email])
                messages.success(request, '編集を依頼しました。')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('question_answer', pk=pk)
        return render(request, 'questionRequest.html', {'form': form, 'allcats': allcats, 'question': question})

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionUpdate(UpdateView):
    template_name = 'questionForm.html'
    model = QuestionModel
    form_class = QuestionForm

# 1/10 アクセス制限
    def get(self, request, *args, **kwargs):
        obj = QuestionModel.objects.get(pk=self.kwargs['pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(QuestionUpdate, self).get(request, *args, **kwargs)

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AnswerUpdate(UpdateView):
    template_name = 'questionAnswer.html'
    model = AnswerModel
    form_class = AnswerForm

# 1/10 アクセス制限
    def get(self, request, *args, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(AnswerUpdate, self).get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        return obj

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = QuestionModel.objects.get(pk=self.kwargs['pk'])
        context["question"] = question
        context["allcats"] = Category.objects.filter(parent=None)
        context["answers"] = AnswerModel.objects.filter(
            question=self.kwargs['pk'])
        context["counts"] = AnswerModel.objects.filter(
            question=self.kwargs['pk']).count()
        return context

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class QuestionDelete(DeleteView):
    model = QuestionModel
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        obj = QuestionModel.objects.get(pk=self.kwargs['pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(QuestionDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context
    
    def get_success_url(self,  **kwargs):
        return reverse("question_list", kwargs={"pk": 1})

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class AnswerDelete(DeleteView):
    model = AnswerModel
    template_name = 'delete.html'

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})

    def get_object(self, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        return obj

# 1/10 アクセス制限
    def get(self, request, *args, **kwargs):
        obj = AnswerModel.objects.get(pk=self.kwargs['answer_pk'])
        if obj.created_by != self.request.user:
            messages.warning(request, "権限がありません")
            return redirect('question_answer', pk=self.kwargs['pk'])
        return super(AnswerDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context
