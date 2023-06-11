from django.urls import path
from . import views

urlpatterns = [
    # 전체 리뷰 다 가져오기(Beta)
    path('review_all/',views.review_all),

    # 단일 리뷰 가져오기
    path('review/<int:review_id>/', views.get_review),

    # 영화 마다 각각의 리뷰 페이지
    path('<int:movie_id>/',views.review_list_or_create),
    path('<int:review_id>/update_or_delete/',views.review_update_or_delete),
    # 댓글
    path('comments/',views.comment_list),
    path('comments/<int:comment_id>/',views.comment_detail),

    # 리뷰 좋아요
    path('<int:review_id>/reviewlikes/',views.reviewlikes),

    # 댓글 생성 ( Vue에서 호출할 함수 )
    path('<int:review_id>/comments/',views.comment_create)
]
