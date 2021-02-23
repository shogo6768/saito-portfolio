from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import PostModel, Category
from accounts.models import Like
from accounts.models import CustomUser 
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
from django.core.exceptions import PermissionDenied
# フォーム定義
from .forms import ContactForm



# logger定義
logger = logging.getLogger(__name__)

# Create your views here.

class TopPage(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はトップ画面へリダイレクト
        allcats = Category.objects.filter(parent=None)
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)
        return render(equest, 'toppage.html', {'allcats': allcats})

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["allcats"] = Category.objects.filter(parent=None)


# 1/14　髙木更新　Historyモデルを使う前提でsave_history関数を書き直し

class PostDetail(DetailView):
    model = PostModel
    template_name = 'post.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public:
            raise Http404
        obj.views += 1
        obj.save()
        return obj

     # 12/19斉藤コメント　カテゴリ-一覧とカテゴリ-別ランキングのcontext追加
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
        context["category_ranking"] = PostModel.objects.filter(
            category_id=self.object.category_id).order_by('-views')
        # 12/27斉藤コメント　関連記事
        context["related_posts"] = PostModel.objects.filter(
            category_id=self.object.category_id).exclude(pk=self.object.pk)
        # 1/19 斉藤追加
        if self.request.user.is_authenticated:
            context["like"] = Like.objects.filter(
                Q(user=self.request.user) & Q(post=self.object))
        return context
         


# def searchfunc(request):
#     allcats = Category.objects.filter(parent=None)
#     # 12/19斉藤コメント　カテゴリ-一覧のため追加
#     # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
#     qs = PostModel.objects.all()
#     key_search = request.GET.get('key_search')
#     if key_search != '' and key_search is not None:
#         qs = qs.filter(Q(title__icontains=key_search)| Q(content__icontains=key_search)).distinct
#     return render(request, "search_result.html", {'allcats': allcats, 'qs': qs})

def searchfunc(request):
    allcats = Category.objects.filter(parent=None)
    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
    key_search = request.GET.get('key_search')
    print(key_search)
    if key_search != '' and key_search is not None:
        qs = PostModel.objects.filter(Q(title__icontains=key_search)| Q(content__icontains=key_search)).distinct
        return render(request, "search_result.html", {'allcats': allcats, 'qs': qs})
    return render(request, "search_result.html", {'allcats': allcats})


class AllContents(TemplateView):
    template_name = 'all_contents.html'

    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


def categoryfunc(request, slug):
    allcats = Category.objects.filter(parent=None)
    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
    category = Category.objects.get(slug=slug)
    category_posts = PostModel.objects.filter(category=category)
    category_ranking = PostModel.objects.filter(
        category=category).order_by('-views')
    return render(request, "category.html", {'allcats': allcats, 'slug': slug, 'category_posts': category_posts, 'category_ranking': category_ranking})

# ランキング機能追加

class RankingList(ListView):
    model = PostModel
    template_name = 'ranking.html'
    paginate_by = 10
    queryset = PostModel.objects.order_by('-views')

    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context
 

def contact(request):
    # allcatsはheaderのためのcontext
    allcats = Category.objects.filter(parent=None)
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact.html', {'form': form, 'allcats': allcats})
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['contact_subject']
            body = {
			    'contact_email' : form.cleaned_data['contact_email'],
                'contact_message' : form.cleaned_data['contact_message']
			}
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'test@em9607.plusit-1.com', ['testplusit@gmail.com'])
                messages.success(request, '貴重なご意見ありがとうございました。')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            if request.user.is_authenticated:
                return redirect('mypage', pk=request.user.id)
            else:
                return redirect('toppage')
        return render(request, 'contact.html', {'form': form, 'allcats': allcats})


