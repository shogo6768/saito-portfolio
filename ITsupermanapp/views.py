from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import PostModel, Category, CustomUser
from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
# 追加インポート
import logging
from django.urls import reverse
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.conf import settings
from django.contrib import messages
# フォーム定義
from .forms import LoginForm, CreateForm

# logger定義
logger = logging.getLogger(__name__)

# Create your views here.
class TopPage(TemplateView):
    template_name='toppage.html'

class PostDetail(DetailView):
    model = PostModel
    template_name = 'post.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

        # 閲覧履歴機能（リコメンドにも使用、未実装のためコメントアウト）
    # def save_history(self, request, pk):
    #     user = CustomUser.objects.get(id = request.user.id)
    #     user.history = pk
    #     user.save()

def searchfunc(request):
    qs = PostModel.objects.all()
    key_search = request.GET.get('key_search')
    if key_search !='' and key_search is not None:
        qs = qs.filter(Q(title__icontains=key_search)
                       | Q(content__icontains=key_search)
                       ).distinct

    return render(request, "search_result.html", {'qs':qs})

class AllContents(TemplateView):
    template_name='all_contents.html'


def postfunc(request):
    qs = PostModel.objects.all()
    key_search = request.GET.get('key_search')
    if key_search !='' and key_search is not None:
        qs = qs.filter(Q(title__icontains=key_search)
                       | Q(content__icontains=key_search)
                       ).distinct

    return render(request, "search_result.html", {'qs':qs})

def categoryfunc(request, cats):
    category = Category.objects.get(slug=cats)
    category_posts = PostModel.objects.filter(category=category)
    return render(request, "category.html", {'cats':cats, 'category_posts':category_posts})

class RankingList(ListView):
    model = PostModel
    template_name = 'ranking.html'
    paginate_by = 10
    queryset= PostModel.objects.order_by('-views')


class CreateView(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はトップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('toppage'))

        context = {
            'form': CreateForm(),
        }
        return render(request, 'accounts/create.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")

        # リクエストからフォームを作成
        form = CreateForm(request.POST)
        # バリデーション
        if not form.is_valid():
            # バリデーションNGの場合はアカウント登録画面のテンプレートを再表示
            return render(request, 'accounts/create.html', {'form': form})

        # 保存する前に一旦取り出す
        user = form.save(commit=False)
        # パスワードをハッシュ化してセット
        user.set_password(form.cleaned_data['password'])
        # ユーザーオブジェクトを保存
        user.save()

        # ログイン処理（取得した Userオブジェクトをセッションに保存 & Userデータを更新）
        auth_login(request, user)

        return redirect(reverse('toppage'))


create = CreateView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('toppage'))

        context = {
            'form': LoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = LoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)

        # # ログイン後処理（ログイン回数を増やしたりする。本来は user_logged_in シグナルを使えばもっと簡単に書ける）
        # user.post_login()
        #
        # # ロギング
        # logger.info("User(id={}) has logged in.".format(user.id))

        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")

        # トップ画面にリダイレクト
        return redirect(reverse('toppage'))


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(id={}) has logged out.".format(request.user.id))
            # ログアウト処理
            auth_logout(request)

        # フラッシュメッセージを画面に表示
        messages.info(request, "ログアウトしました。")

        return redirect(reverse('toppage'))


logout = LogoutView.as_view()


# お気に入り機能用のビュー
# post.html内の"お気に入りボタン"を押されるとCustomUserモデルのlike_postフィールドに格納される
def like(request, pk):
    post = PostModel.objects.get(pk=pk)
    request.user.like_post.add(post)
    return redirect(reverse('toppage'))

# マイページアップデート
# お気に入り記事の一覧を取得し、表示できる様に変更（デザインは後回し）
class MypageView(View):
    model = CustomUser

    def get(self, request, pk, *args, **kwargs):
        like_posts=request.user.like_post.all()
        return render(request, 'accounts/mypage.html', {'like_posts':like_posts})

mypage = MypageView.as_view()
