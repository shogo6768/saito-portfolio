from django.urls import path
from .views import TopPage, PostDetail, save_history, searchfunc, like, AllContents, categoryfunc, CreateView, LoginView, MypageView, LogoutView, RankingList, contact, success

urlpatterns = [
    path('', TopPage.as_view(), name='toppage'),
    # # save_history関数のディスパッチャ
    path('post/<int:pk>', save_history, name='save_history'),
    # PostDetailへのURL構造を小変更
    # 12/19斉藤コメント　nameを変更を関連urlも修正。またpath末尾に'/'追加（エラー回避のため）
    path('post/<int:pk>/detail/', PostDetail.as_view(), name='post_detail'),
    # likeへのディスパッチャ
    path('post/<int:pk>/like', like, name='like'),
    path('searchresult/',  searchfunc, name='search'),
    path('all_contents/', AllContents.as_view(), name='all_contents'),
    path('category/<str:cats>/', categoryfunc, name='category'),
    path('ranking/', RankingList.as_view(), name='ranking'),
    path('create/', CreateView.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/<int:pk>/', MypageView.as_view(), name='mypage'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
]
