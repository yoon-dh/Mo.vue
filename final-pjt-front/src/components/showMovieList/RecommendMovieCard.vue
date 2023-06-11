<template>
  <div id="app3">
    <div class="full_card_layout">
      <h1 id="movie-title">{{ movie.title }}({{ movie.original_title }})</h1>
      <div class="movie-card">
        <div class="movie-card-info">
          <div class="movie-card-info-first">
            <img
              class="movie-card-poster"
              :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`"
              alt="영화 포스터"
            />
            <div class="movie-card-info-detail">
              <p>평점 : {{ movie?.vote_average.toFixed(1) }}</p>
              <p>
                장르 :
                <span v-for="(genre, index) in genres" :key="genre">
                  {{ genre }}
                  <span v-if="index !== genres.length - 1">,</span>
                </span>
              </p>
              <p>감독 : {{ director }}</p>
              <p>
                출연진 :<span
                  v-for="(actor, index) in actors"
                  :key="actor.original_name"
                >
                  {{ actor.original_name }}
                  <span v-if="index !== actors.length - 1">,</span>
                </span>
              </p>
              <p>개봉일 : {{ movie.release_date }}</p>

              <button
                class="button button-like"
                :class="{ liked: movie_liked }"
                @click="movielike"
              >
                <i class="fa fa-heart"></i>
                <span>Like</span>
              </button>
            </div>
          </div>

          <div class="movie-card-info-overview">
            <p>{{ movie.overview }}</p>
          </div>
        </div>

        <div class="comments-space">
          <div class="comment-button-space">
            <button class="comment-button" @click="popupOpen">
              Write Review
            </button>
            <button class="comment-button" @click="toReview">
              More Review
            </button>
          </div>
          <div class="movie-card-comments">
            <swiper class="swiper movie-comment" :options="swiperOption">
              <MovieShortReview
                v-for="shortreview in shortreviewList"
                :key="shortreview.id"
                :shortreview="shortreview"
              />
            </swiper>
          </div>
        </div>
      </div>

      <!-- Review-write-popup -->
      <div class="black-bg-top" v-if="isReviewPopup">
        <div class="white-bg-top">
          <ReviewPopup class="popup-top" :movieID="top_recommend_movie" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ReviewPopup from "@/components/PopupList/ReviewPopup.vue";
import MovieShortReview from "@/components/ReviewList/MovieShortReview.vue";

import { Swiper } from "vue-awesome-swiper";
import "swiper/css/swiper.css";
import axios from "axios";

export default {
  name: "RecommendMovieCard",
  components: {
    ReviewPopup,
    MovieShortReview,
    Swiper,
  },
  props: {
    top_recommend_movie: Number,
  },
  methods: {
    toReview() {
      const movieId = this.top_recommend_movie;
      this.$router.push({ name: "review", params: { id: movieId } });
    },
    popupOpen() {
      console.log(this.top_recommend_movie);
      const realID = this.top_recommend_movie;
      this.$store.commit("REVIEW_POPUP_OPEN");
      this.$store.commit("TOPTEN_REVIEW_ID", realID);
    },

    movielike() {
      const movieID = this.top_recommend_movie;
      console.log(movieID);
      console.log(typeof movieID);

      axios({
        method: "post",
        url: `http://127.0.0.1:8000/movies/${movieID}/movielikes/`,
        headers: {
          Authorization: `Token ${this.$store.state.token}`,
        },
      }).then((res) => {
        this.movie_liked = res.data.liked;
        this.movie_liked_count = res.data.like_count;
      });
    },
  },

  created() {
    const movieID = this.top_recommend_movie;
    const API_KEY = process.env.VUE_APP_TMDB_API_KEY;

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieID}?api_key=${API_KEY}&language=ko-KR`,
    }).then((res) => {
      const movieData = res.data;
      this.movie = movieData;

      for (let i = 0; i < movieData.genres.length; i++) {
        this.genres.push(movieData.genres[i].name);
      }
    });

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieID}/credits?api_key=${API_KEY}&language=en-US`,
    })
      .then((res) => {
        this.actors.push(res.data.cast[0]);
        this.actors.push(res.data.cast[1]);
        this.actors.push(res.data.cast[2]);

        const crew = res.data.crew;
        for (let i = 0; i < crew.length - 1; i++) {
          if (crew[i].job === "Director") {
            this.director = crew[i].name;
            return;
          }
        }
      })
      .catch(() => {});

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/${movieID}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        const reviewALL = res.data;
        const groupedArray = [];

        for (let i = 0; i < reviewALL.length; i += 4) {
          if (i + 4 >= reviewALL.length) {
            groupedArray.push(reviewALL.slice(i));
          } else {
            groupedArray.push(reviewALL.slice(i, i + 4));
          }
        }
        this.shortreviewList = groupedArray;
      })
      .catch(() => {
        this.shortreviewList = [];
      });

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/movies/${movieID}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        const requestUser = this.$store.state.userID;
        const likeUserList = res.data.like_users;
        for (let i = 0; i < likeUserList.length; i++) {
          if (likeUserList[i] === requestUser) {
            this.movie_liked = true;
            return;
          }
        }
        this.movie_liked = false;
      })
      .catch(() => {});
  },

  data() {
    return {
      movie: [],
      actors: [],
      director: null,
      genres: [],
      shortreviewList: null,
      movie_liked: null,
      movie_liked_count: null,
    };
  },

  computed: {
    isReviewPopup() {
      return this.$store.state.isReviewPopup;
    },

    swiperOption() {
      return {
        slidesPerView: 1,
        spaceBetween: 300,
        loop: true,
        autoplay: {
          delay: 15000,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      };
    },

    C_director() {
      return this.director;
    },
  },
};
</script>

<style></style>
