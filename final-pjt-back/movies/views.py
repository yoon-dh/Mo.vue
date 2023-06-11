from django.shortcuts import render,get_list_or_404,get_object_or_404
import json
import requests
from django.http import HttpResponse
from .serializers import  MovieListSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Movie
from accounts.models import User

# 알고리즘용 
from collections import Counter
from itertools import combinations
import random


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie(request,movie_id):
    movie = get_object_or_404(Movie, movie_id = movie_id)
    serializer = MovieListSerializer(movie)
    return Response(serializer.data)



# 각각의 유저가 좋아하는 영화 리스트 받아오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usermovielikes(request):
    user = request.user
    if request.method == 'GET':
        user_like_movie = user.like_movies
        serializer = MovieListSerializer(user_like_movie, many=True)
        return Response(serializer.data)

# =======================================================================================

# 영화 알고리즘 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_movie(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'GET':
        user_like_movie = user.like_movies
        serializer = MovieListSerializer(user_like_movie, many=True)
        like_movie_list = serializer.data

        movieALL = get_list_or_404(Movie)
        movieAll_data = MovieListSerializer(movieALL, many = True)
        All_Movie_List = list(movieAll_data.data)
        # 평점 기준 정렬
        All_Movie_Sort = sorted(All_Movie_List, key = lambda x : -x['vote_average'])


        like_movie_id = []
        like_movie = []

        for i in range(len(like_movie_list)):
            like_movie += like_movie_list[i]['genres'].lstrip('[').rstrip(']').split(',')
            like_movie_id.append(like_movie_list[i]['movie_id'])
        

        like_movie_counter = Counter(like_movie)
        top3 = sorted(like_movie_counter.items(),key=lambda x:-x[1])

        print('=====================================')
        print('=====================================')
        print(like_movie_counter)
        print('=====================================')
        print('=====================================')

        # 좋아하는 영화의 장르가 없으면 랜덤 10개
        if len(top3) == 0:
            random_movies = random.sample(All_Movie_Sort, 10)
            return Response([i['movie_id'] for i in random_movies])

        # 좋아하는 영화의 장르가 3개 이하면 그냥 가장 좋아하는 장르 영화로 10개 추천
        # 1. vote_count는 최소 100이상
        # 2. vote_average는 7이상
        if len(top3) < 3:
            reco_list = []
            favorite = top3[0][0] 
            for i in range(len(All_Movie_Sort)):
                if favorite in All_Movie_Sort[i]['genres'] and All_Movie_Sort[i]['vote_count'] >= 100:
                    if All_Movie_Sort[i]['movie_id'] not in like_movie_id:
                        reco_list.append(All_Movie_Sort[i]['movie_id'])
                        if len(reco_list) == 10:
                            break

            return Response(reco_list)


        # 좋아하는 영화 장르가 3개 이상이면 ( vote_count >= 100 and vote_average >= 7 )
        # 1순위 3개 전부 포함
        # 2순위 2개 포함
        # 3순위 1개 포함
        else: 
            top3_genres = top3[:3]
            top3_list = [top3[0][0],top3[1][0],top3[2][0]]
            
            reco_list = []
            
            for i in range(len(All_Movie_Sort)):
                if All_Movie_Sort[i]['vote_count'] >= 100 and All_Movie_Sort[i]['vote_average'] >= 7:
                    if All_Movie_Sort[i]['movie_id'] not in like_movie_id:
                        cnt = 0
                        for j in top3_list:
                            if j in All_Movie_Sort[i]['genres']:
                                cnt += 1

                        if cnt == 3: 
                            reco_list.append((All_Movie_Sort[i]['movie_id'],All_Movie_Sort[i]['title'],cnt,All_Movie_Sort[i]['vote_average']))
                        elif cnt == 2: 
                            reco_list.append((All_Movie_Sort[i]['movie_id'],All_Movie_Sort[i]['title'],cnt,All_Movie_Sort[i]['vote_average']))


            if len(reco_list) < 10:
                favorite = top3[0][0]
                for i in range(len(All_Movie_Sort)):
                    if All_Movie_Sort[i]['vote_count'] >= 100 and All_Movie_Sort[i]['vote_average'] >= 7 and favorite in All_Movie_Sort[i]['genres']:
                        if All_Movie_Sort[i]['movie_id'] not in [i[0] for i in reco_list]:
                            if All_Movie_Sort[i]['movie_id'] not in like_movie_id:
                                reco_list.append((All_Movie_Sort[i]['movie_id'],All_Movie_Sort[i]['title'],cnt,All_Movie_Sort[i]['vote_average']))
                                if len(reco_list) == 10:
                                    break

            if len(reco_list) < 10:
                favorite = top3[1][0]

                for i in range(len(All_Movie_Sort)):
                    if All_Movie_Sort[i]['vote_count'] >= 100 and All_Movie_Sort[i]['vote_average'] >= 7 and favorite in All_Movie_Sort[i]['genres']:
                        if All_Movie_Sort[i]['movie_id'] not in [i[0] for i in reco_list]:
                            if All_Movie_Sort[i]['movie_id'] not in like_movie_id:
                                reco_list.append((All_Movie_Sort[i]['movie_id'],All_Movie_Sort[i]['title'],cnt,All_Movie_Sort[i]['vote_average']))
                                if len(reco_list) == 10:
                                    break

            sort_reco_list = sorted(reco_list, key = lambda x : (-x[2],-x[3]))[0:10]

            return Response([i[0] for i in sort_reco_list])

# =======================================================================================
    


# 영화 좋아요 누르기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movielikes(request,movie_pk):
    if not Movie.objects.filter(pk=movie_pk).exists():
        TMDB_api_key='d5ac433b50437f709a1b781ee653c566'

        url = f'https://api.themoviedb.org/3/movie/{movie_pk}?api_key={TMDB_api_key}&language=ko-KR'
        data = requests.get(url).json()

        movie_id = data['id']
        title = data['title']
        overview = data['overview']
        release_date = data['release_date']
        poster_path = data['poster_path']
        popularity = data['popularity']
        runtime = data['runtime']
        genre_list = data['genres']
        backdrop_path = data['backdrop_path']
        status = data['status']
        vote_average = data['vote_average']
        vote_count = data['vote_count']
        adult = data['adult']
        genres = []
        for genre in genre_list:
            genres.append(genre['name'])

        Movie.objects.create(
                        movie_id = movie_id,
                        title = title,
                        overview = overview,
                        release_date = release_date,
                        poster_path = poster_path,
                        popularity = popularity,
                    
                        genres = genres,
                        runtime = runtime,
                        backdrop_path = backdrop_path,
                        status = status,
                        vote_average = vote_average,
                        vote_count = vote_count,
                        adult = adult,
                    )
    
    movie = get_object_or_404(Movie, movie_id = movie_pk)
    user = request.user
    
    if request.method == 'POST':
        if movie.like_users.filter(pk = user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        context = {
            'liked' : liked,
            'like_count' : movie.like_users.count()
        }

        return Response(context)


def movie_data_update(request):
    TMDB_api_key='d5ac433b50437f709a1b781ee653c566'
    nums = range(1,50000) # 시간 너무 오래 걸려서 일단 10000
    for num in nums:
        try:
            video_url = f'https://api.themoviedb.org/3/movie/{num}/videos?api_key={TMDB_api_key}&language=ko-KR'
            video = requests.get(video_url).json()
            if video['results']:
                video_id = video['results'][0]['key']     # 추후 vue의 iframe api 요청보낼때의 video_id 값
                
                url = f'https://api.themoviedb.org/3/movie/{num}?api_key={TMDB_api_key}&language=ko-KR'
                data = requests.get(url).json()
                movie_id = data['id']
                title = data['title']
                overview = data['overview']
                release_date = data['release_date']
                poster_path = data['poster_path']
                popularity = data['popularity']
                runtime = data['runtime']
                genre_list = data['genres']
                backdrop_path = data['backdrop_path']
                status = data['status']
                vote_average = data['vote_average']
                vote_count = data['vote_count']
                adult = data['adult']
                genres = []
                for genre in genre_list:
                    genres.append(genre['name'])

                Movie.objects.create(
                    movie_id = movie_id,
                    title = title,
                    overview = overview,
                    release_date = release_date,
                    poster_path = poster_path,
                    popularity = popularity,
                    video_id = video_id,
                    genres = genres,
                    runtime = runtime,
                    backdrop_path = backdrop_path,
                    status = status,
                    vote_average = vote_average,
                    vote_count = vote_count,
                    adult = adult,
                )
            else:
                pass
        except:
            pass
    return JsonResponse(data)

