from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
# from django.views.generic.edit import CreateView
from .models import PostModel, Category, CustomUser,  QuestionModel, AnswerModel, RequestModel, Like, History
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
from .forms import LoginForm, CreateForm, ContactForm, QuestionForm, AnswerForm, RequestForm
from django import template

# logger定義
logger = logging.getLogger(__name__)

# Create your views here.


class TopPage(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はトップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)
        return render(request, 'toppage.html', {})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)


# 1/14　髙木更新　Historyモデルを使う前提でsave_history関数を書き直し


def save_history(request, pk):
    user = request.user
    look_post = PostModel.objects.get(pk=pk)
    history = History.objects.filter(Q(user=user) & Q(post=look_post))

    if history:
        history.delete()
        history = History.objects.create(user=user, post=look_post)
    else:
        history = History.objects.create(user=user, post=look_post)

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
        context["like"] = Like.objects.filter(
            Q(user=self.request.user) & Q(post=self.object))
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


class CreateUser(View):
    def get(self, request, *args, **kwargs):
        # すでにログインしている場合はマイページへリダイレクト
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)
        context = {'form': CreateForm()}
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

        return redirect('mypage', pk=request.user.id)


# create = CreateView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # 1/4 斉藤allcats追加
        allcats = Category.objects.filter(parent=None)
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect('mypage', pk=request.user.id)

        # 1/4 斉藤allcats追加
        context = {
            'form': LoginForm(),
            'allcats': allcats
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
        # フラッシュメッセージを画面に表示
        messages.info(request, "ログインしました。")

        return redirect('mypage', pk=request.user.id)


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


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
# 1/14　髙木更新　Likeモデルを使う前提でlike関数を書き直し
def like(request, pk):
    post = PostModel.objects.get(pk=pk)
    user = request.user
    like_object = Like.objects.filter(Q(user=user) & Q(post=post))
    if like_object:
        like_object.delete()
    else:
        like_object = Like.objects.create(user=user, post=post)
    return redirect('post_detail', pk=pk)

# マイページアップデート
# お気に入り記事の一覧を取得し、表示できる様に変更（デザインは後回し）
# 1/14　髙木更新　Like, Historyモデルの活用で時系列順の表示可能に。


class MypageView(View):
    model = CustomUser

    def get(self, request, pk, *args, **kwargs):
        # 1/14　髙木更新　Like、Historyをモデルに変更により、context作成のアルゴリズム変更
        likes = Like.objects.filter(user=request.user).order_by('-created_at')
        histories = History.objects.filter(
            user=request.user).order_by('-created_at')
        recommend_posts = PostModel.objects.none()
        cats = []
        histories_for_recommend = histories.order_by('-created_at')[:3]

        # 1/4 斉藤追加
        allcats = Category.objects.filter(parent=None)

        for history in histories_for_recommend:
            cat = history.post.category
            cats.append(cat)
        cats_unique = list(set(cats))

        # 12/30　recommend_postsのクエリセットにカテゴリーから取得したオススメ記事のクエリセットを結合(chain関数　インポート必要)
        for cat in cats_unique:
            posts = PostModel.objects.filter(
                category=cat).order_by('-created_at')[:3]
            recommend_posts = chain(recommend_posts, posts)

        return render(request, 'accounts/mypage.html', {'like_posts': likes, 'history_posts': histories, 'recommend_posts': recommend_posts, 'allcats': allcats})


# 1/14　髙木更新　退会機能系の３種を追加


class Resign(TemplateView):
    template_name = 'accounts/resign.html'


class ResConduct(View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            return redirect(reverse('resign_complete'))


class ResComplete(TemplateView):
    template_name = 'accounts/resign_complete.html'


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
                messages.success(request, '貴重なご意見ありがとうございました。')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('mypage', pk=request.user.id)
        return render(request, 'contact.html', {'form': form, 'allcats': allcats})


# 1/4　斉藤コメント　以降Q&A関連
class QuestionCreate(CreateView):
    template_name = 'questionForm.html'
    model = QuestionModel
    form_class = QuestionForm
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context


class QuestionList(ListView):
    template_name = 'questionList.html'
    paginate_by = 5
    queryset = PostModel.objects.order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = QuestionModel.objects.all()
        context["questions"] = question
        context["allcats"] = Category.objects.filter(parent=None)
        return context


def questionAnswer(request, pk):
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
        'question': question,
        'answers': answers,
        'form': answer_form,
        'counts': counts
    })

# 1/10 編集request追加


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
            from_email = "shogo6768@gmail.com"
            to_email = QuestionModel.objects.get(pk=pk).created_by.email
            try:
                send_mail(request_subject, request_message,
                          from_email, [to_email])
                messages.success(request, '送信完了しました。')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('question_answer', pk=pk)
        return render(request, 'questionRequest.html', {'form': form, 'allcats': allcats, 'question': question})


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["allcats"] = Category.objects.filter(parent=None)
        return context

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse("question_answer", kwargs={"pk": pk})


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


class QuestionDelete(DeleteView):
    model = QuestionModel
    success_url = reverse_lazy('question_list')
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
