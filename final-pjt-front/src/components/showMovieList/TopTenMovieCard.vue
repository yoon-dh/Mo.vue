<template>
  <div id="app3">
    <div class="full_card_layout">
      <h1 id="movie-title">
        {{ top_recommend_movie.title }}({{
          top_recommend_movie.original_title
        }})
      </h1>
      <div class="movie-card">
        <div class="movie-card-info">
          <div class="movie-card-info-first">
            <img
              class="movie-card-poster"
              :src="`https://image.tmdb.org/t/p/original/${top_recommend_movie.poster_path}`"
              alt="영화 포스터"
            />
            <div class="movie-card-info-detail">
              <p>평점 : {{ top_recommend_movie.vote_average.toFixed(1) }}</p>
              <p>
                장르 :
                <span v-for="(genre, index) in genres" :key="genre">
                  {{ genre }}
                  <span v-if="index !== genres.length - 1">,</span>
                </span>
              </p>
              <p>감독 : {{ C_director }}</p>
              <p>
                출연진 :<span
                  v-for="(actor, index) in actors"
                  :key="actor.original_name"
                >
                  {{ actor.original_name }}
                  <span v-if="index !== actors.length - 1">,</span>
                </span>
              </p>
              <p>개봉일 : {{ top_recommend_movie.release_date }}</p>

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
            <p>{{ top_recommend_movie.overview }}</p>
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
          <ReviewPopup class="popup-top" :movieID="movieIDD" />
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
  name: "App",
  components: {
    ReviewPopup,
    MovieShortReview,
    Swiper,
  },
  props: {
    top_recommend_movie: Object,
    movieIDD: Number,
  },

  methods: {
    toReview() {
      const movieId = this.top_recommend_movie.id;
      this.$router.push({ name: "review", params: { id: movieId } });
    },
    popupOpen() {
      const realID = this.movieIDD;
      this.$store.commit("REVIEW_POPUP_OPEN");
      this.$store.commit("TOPTEN_REVIEW_ID", realID);
    },

    movielike() {
      const movieID = this.movieIDD;

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
    const movieId = this.top_recommend_movie.id;
    const API_KEY = process.env.VUE_APP_TMDB_API_KEY;

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieId}?api_key=${API_KEY}&language=ko-KR`,
    }).then((res) => {
      const movieData = res.data;
      this.movie = movieData;

      for (let i = 0; i < movieData.genres.length; i++) {
        this.genres.push(movieData.genres[i].name);
      }
    });

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieId}/credits?api_key=${API_KEY}&language=en-US`,
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
      .catch((err) => {
        console.log(err);
      });

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/${movieId}/`,
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
      url: `http://127.0.0.1:8000/movies/${movieId}/`,
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

<style>
#app3 {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #dce9f7;
  padding: 60px 20px 0px 20px;
  border-radius: 20px 20px 0px 0px;
  border: 1px solid white;
}

.movie-bg-img {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 70vw;
  z-index: -1;
  filter: brightness(0.3);
}

#movie-title {
  text-align: center;
  margin: 40px;
}

.movie-card {
  display: flex;
}

.movie-card-info {
  background: rgb(27, 26, 26);
  opacity: 0.85;
  border-radius: 2% 0% 0% 2%;
  flex: 1;
  display: flex;

  height: 80%;
  flex-direction: column;
  padding: 30px;
}

.movie-card-info-first {
  display: flex;
  flex-direction: row;
}

.movie-card-poster {
  width: 20vw;
  margin: 10px 0px 10px 10px;
  border-radius: 8px;
}

.movie-card-info-detail {
  margin: 40px;
  text-align: left;
}

.movie-card-info-overview {
  margin: 10px;
  padding: 20px;
}

.top-ten-comments-space {
  border: 20px solid rgb(24, 23, 23);
  flex: 1;
  border-radius: 4% 4% 0% 0%;
}
.top-ten-movie-card-comments {
  background-color: rgb(243, 243, 243);
  height: 100%;
  padding: 30px;
  text-align: left;

  background-size: 540% 540%;
  animation: gradient-animation 30s ease infinite;
}

@keyframes gradient-animation {
  0% {
    background-position: 0% 30%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 40%;
  }
}

/* Review PopUP */

.black-bg-top {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.white-bg-top {
  position: relative;
  width: 100%;
  height: 100%;
}

.popup-top {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 2px 7px rgba(0, 0, 0, 0.05);
}

.button-like {
  border: 2px solid #c12d2d;
  background-color: transparent;
  text-decoration: none;
  padding: 10px;
  position: relative;
  vertical-align: middle;
  text-align: center;
  display: inline-block;
  border-radius: 3rem;
  color: #8a8a8a;
  transition: all ease 0.4s;
}

.button-like span {
  margin: 0.8rem;
}

.button-like .fa,
.button-like span {
  transition: all ease 0.4s;
  margin-left: 0.5rem;
}

.button-like:focus {
  background-color: transparent;
}

.button-like:focus .fa,
.button-like:focus span {
  color: #8a8a8a;
}

.button-like:hover {
  border-color: #cc4b37;
  background-color: transparent;
}

.button-like:hover .fa,
.button-like:hover span {
  color: #cc4b37;
}

.liked {
  background-color: #cc4b37;
  border-color: #cc4b37;
}

.liked .fa,
.liked span {
  color: #fefefe;
}

.liked:focus {
  background-color: #cc4b37;
}

.liked:focus .fa,
.liked:focus span {
  color: #fefefe;
}

.liked:hover {
  background-color: #cc4b37;
  border-color: #cc4b37;
}

.liked:hover .fa,
.liked:hover span {
  color: #fefefe;
}
</style>
