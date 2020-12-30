from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import PostModel, Category, CustomUser
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
# メール送信のための追加インポート
from django.core.mail import send_mail, BadHeaderError
# 追加インポート
import logging
from django.urls import reverse
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.conf import settings
from django.contrib import messages
from itertools import chain
# フォーム定義
from .forms import LoginForm, CreateForm, ContactForm

# logger定義
logger = logging.getLogger(__name__)

# Create your views here.


class TopPage(TemplateView):
    template_name = 'toppage.html'

# save_history関数を外へ


def save_history(request, pk):
    post = PostModel.objects.get(pk=pk)
    request.user.history.add(post)
    request.user.save()
    return redirect('post_detail', pk=pk)


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
        return context


def searchfunc(request):
    allcats = Category.objects.filter(parent=None)
    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
    qs = PostModel.objects.all()
    key_search = request.GET.get('key_search')
    if key_search != '' and key_search is not None:
        qs = qs.filter(Q(title__icontains=key_search)
                       | Q(content__icontains=key_search)
                       ).distinct
    return render(request, "search_result.html", {'allcats': allcats, 'qs': qs})


class AllContents(TemplateView):
    template_name = 'all_contents.html'

    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


def categoryfunc(request, cats):
    allcats = Category.objects.filter(parent=None)
    # 12/19斉藤コメント　カテゴリ-一覧のため追加
    # parent=Noneによって親が空のcategoryを表示。つまり親カテゴリーのみ表示
    category = Category.objects.get(slug=cats)
    category_posts = PostModel.objects.filter(category=category)
    category_ranking = PostModel.objects.filter(
        category=category).order_by('-views')
    return render(request, "category.html", {'allcats': allcats, 'cats': cats, 'category_posts': category_posts, 'category_ranking': category_ranking})


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


# お気に入り機能用のビュー
# post.html内の"お気に入りボタン"を押されるとCustomUserモデルのlike_postフィールドに格納される
# 12/30　高木更新　like関数が呼ばれたときに既にお気に入りに登録あれば解除する
def like(request, pk):
    post = PostModel.objects.get(pk=pk)
    if request.user.like_post.filter(pk=post.pk):
        request.user.like_post.remove(post)
    else:
        request.user.like_post.add(post)
    return redirect('post_detail', pk=pk)

# マイページアップデート
# お気に入り記事の一覧を取得し、表示できる様に変更（デザインは後回し）


class MypageView(View):
    model = CustomUser

    def get(self, request, pk, *args, **kwargs):
        like_posts = request.user.like_post.all()
        history_posts = request.user.history.all()

        recommend_posts = PostModel.objects.none()
        cats = []

        for post in history_posts:
            cat = post.category
            cats.append(cat)

        cats_unique = list(set(cats))

        # 12/30　recommend_postsのクエリセットにカテゴリーから取得したオススメ記事のクエリセットを結合(chain関数　インポート必要)
        for cat in cats_unique:
            posts = PostModel.objects.filter(
                category=cat).order_by('-created_at')[:3]
            recommend_posts = chain(recommend_posts, posts)

        return render(request, 'accounts/mypage.html', {'like_posts': like_posts, 'history_posts': history_posts, 'recommend_posts': recommend_posts})


mypage = MypageView.as_view()

# 12/27　斉藤コメント　コンタクトフォーム


def contact(request):
    # allcatsはheaderのためのcontext
    allcats = Category.objects.filter(parent=None)
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact.html', {'form': form, 'allcats': allcats})
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_subject = form.cleaned_data['contact_subject']
            contact_email = form.cleaned_data['contact_email']
            contact_message = form.cleaned_data['contact_message']
            try:
                send_mail(contact_subject, contact_message,
                          contact_email, ['shogo6768@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
        return render(request, 'contact.html', {'form': form, 'allcats': allcats})

# 12/27　斉藤コメント　コンタクトフォーム送信後の遷移ページ。遷移場所は要相談


def success(request):
    allcats = Category.objects.filter(parent=None)
    return render(request, 'success.html', {'allcats': allcats})
