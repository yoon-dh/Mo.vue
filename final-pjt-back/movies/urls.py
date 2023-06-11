from django.urls import path
from . import views

urlpatterns = [
    path('',views.movie_list),

    # 단일 영화 데이터
    path('<int:movie_id>/',views.get_movie),

    # 영화 좋아요
    path('<int:movie_pk>/movielikes/', views.movielikes),

    # 각각의 유저가 좋아하는 영화 리스트 받아오기
    path('movielikes/', views.usermovielikes),

    # 영화 데이터 로드
    path('movie_data_update/',views.movie_data_update),

    # 영화 추천 알고리즘
    path('recommend/<int:user_id>/', views.recommend_movie),
]
