from django.urls import path
from .views import TopPage, PostDetail, save_history, searchfunc, like, AllContents, categoryfunc,\
                    CreateUser, LoginView, MypageView, LogoutView, RankingList, contact, success, \
                    QuestionCreate, QuestionList, questionAnswer, QuestionUpdate, AnswerUpdate,\
                    QuestionDelete,  AnswerDelete

urlpatterns = [
    path('', TopPage.as_view(), name ='toppage'),
    # # save_history関数のディスパッチャ
    path('post/<int:pk>', save_history, name='save_history'),
    # PostDetailへのURL構造を小変更
    # 12/19斉藤コメント　nameを変更を関連urlも修正。またpath末尾に'/'追加（エラー回避のため）
    path('post/<int:pk>/detail/', PostDetail.as_view(), name='post_detail'),
    # likeへのディスパッチャ
    path('post/<int:pk>/like', like, name='like'),
    path('searchresult/',  searchfunc, name='search'),
    path('all_contents/', AllContents.as_view(), name ='all_contents'),
    path('category/<str:cats>/', categoryfunc, name ='category'),
    path('ranking/', RankingList.as_view(), name='ranking' ),
    path('create/', CreateUser.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/<int:pk>', MypageView.as_view(), name='mypage'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('question_form/', QuestionCreate.as_view(), name='question_form'),
    path('question_list/', QuestionList.as_view(), name='question_list'),
    path('question_answer/<int:pk>', questionAnswer, name='question_answer'),
    path('question_answer/<int:pk>/question_update', QuestionUpdate.as_view(), name='question_update'),
    path('question_answer/<int:pk>/answer_update/<int:answer_pk>', AnswerUpdate.as_view(), name='answer_update'),
    path('question_answer/<int:pk>/question_delete', QuestionDelete.as_view(), name='question_delete'),
    path('question_answer/<int:pk>/answer_delete/<int:answer_pk>', AnswerDelete.as_view(), name='answer_delete'),
]


