from django.urls import path
# like追加
from .views import TopPage, PostDetail, searchfunc, like, AllContents, categoryfunc, CreateView, LoginView, MypageView, LogoutView, RankingList

urlpatterns = [
    path('', TopPage.as_view(), name ='toppage'),
    path('post/<int:pk>', PostDetail.as_view(), name='PostDetail'),
    # likeへのディスパッチャ
    path('post/<int:pk>/like', like, name='like'),
    path('searchresult/', searchfunc, name='search'),
    path('all_contents/', AllContents.as_view(), name ='all_contents'),
    path('category/<str:cats>/', categoryfunc, name ='category'),
    path('ranking/', RankingList.as_view(), name='ranking' ),
    path('create/', CreateView.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/<int:pk>', MypageView.as_view(), name='mypage'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
