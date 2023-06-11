from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewSerializers,ReviewListSerializers,CommentSerailizer
from .models import Review,Comment
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

# 리뷰 전체 조회(Beta)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def review_all(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializer = ReviewListSerializers(reviews,many=True)
        return Response(serializer.data)

# 단일 리뷰 조회

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_review(request,review_id):
    if request.method == 'GET':
        review = get_object_or_404(Review, id = review_id)
        serializer = ReviewSerializers(review)
        return Response(serializer.data)


# 게시글 조회, 생성
@api_view(['GET','POST',])
@permission_classes([IsAuthenticated])
def review_list_or_create(request,movie_id):
    if request.method == 'GET':
        reviews = get_list_or_404(Review,movie_id = movie_id)
        serializer = ReviewListSerializers(reviews, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewSerializers(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


#게시글 삭제, 수정 
@api_view(['DELETE',])
def review_update_or_delete(request,review_id):
    review = get_object_or_404(Review,id = review_id)
    if request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 리뷰 좋아요

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def reviewlikes(request,review_id):
    review =get_object_or_404(Review,pk = review_id)
    user = request.user

    if request.method == 'GET':
        user_like_review = user.like_reviews
        serializer = ReviewListSerializers(user_like_review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if review.like_users.filter(pk = user.pk).exists():
            review.like_users.remove(user)
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        context = {
            'liked' : liked,
            'like_count' : review.like_users.count()
        }

        return Response(context)




# 댓글 조회 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment_list(request):
    comments = get_list_or_404(Comment) 
    serializers = CommentSerailizer(comments, many = True)
    return Response(serializers.data)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request,comment_id):
    comment = get_object_or_404(Comment,id = comment_id)
    if request.method == 'GET':
        serializer = CommentSerailizer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request,review_id):
    review = get_object_or_404(Review,id = review_id)
    serializer = CommentSerailizer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(review = review, user = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


