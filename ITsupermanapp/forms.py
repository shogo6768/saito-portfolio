from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, QuestionModel, AnswerModel

class CreateForm(forms.ModelForm):
    """ユーザー登録画面用のフォーム"""

    class Meta:
        # 利用するモデルクラスを指定
        model = CustomUser
        # 利用するモデルのフィールドを指定
        fields = ('username', 'email', 'password',)
        # ウィジェットを上書き
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
        }

    password2 = forms.CharField(
        label='確認用パスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フィールドの属性を書き換え emailに必須設定をする
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 3:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 3})
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが合致しません")
        # ユニーク制約を自動でバリデーションしてほしい場合は super の clean() を明示的に呼び出す
        super().clean()


class LoginForm(forms.Form):
    """ログイン画面用のフォーム"""

    username = UsernameField(
        label='ユーザー名',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名', 'autofocus': True}),
    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean_username(self):
        value = self.cleaned_data['username']
        if len(value) < 3:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください', params={'min_length': 3})
        return value

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しいユーザー名を入力してください")
        # パスワードはハッシュ化されて保存されているので平文での検索はできない
        if not user.check_password(password):
            raise forms.ValidationError("正しいユーザー名とパスワードを入力してください")
        # 取得したユーザーオブジェクトを使い回せるように内部に保持しておく
        self.user_cache = user

    def get_user(self):
        return self.user_cache


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True)
        self.fields['last_name'].widget.attrs = {'placeholder': '苗字'}
        self.fields['first_name'].widget.attrs = {'placeholder': '名前'}

    def clean_username(self):
        value = self.cleaned_data['username']
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        return value

# 12/27斉藤コメント　コンタクトフォーム 
class ContactForm(forms.Form):
    contact_email = forms.EmailField(
        required=True, 
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
    )
    contact_subject = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': '件名'}),
    )
    contact_message = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'メッセージ'}),
    )

# CSSのためのクラス
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_email'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['contact_subject'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['contact_message'].widget.attrs['class'] = 'Form-Item-Textarea'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ('title', 'category', 'tags' , 'content',)
        labels = {
            'title': '',
            'category': '',
            'tags': '',
            'content': '',
        }
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['category'].widget.attrs['class'] = 'Form-Item-Select'
        self.fields['tags'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['content'].widget.attrs['class'] = 'Form-Item-Textarea'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = ('answer',)
        labels = {
            'answer': '',
        }

