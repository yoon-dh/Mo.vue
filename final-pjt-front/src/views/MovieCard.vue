<template>
  <div id="app2">
    <div class="upper-space"></div>
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
              <p>평점 : {{ movie.vote_average.toFixed(1) }}</p>
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
      <div class="black-bg" v-if="isReviewPopup">
        <div class="white-bg">
          <ReviewPopup class="popup" :movieID="Number(this.$route.params.id)" />
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

  methods: {
    toReview() {
      const movieId = Number(this.$route.params.id);
      this.$router.push({ name: "review", params: { id: movieId } });
    },
    popupOpen() {
      this.$store.commit("REVIEW_POPUP_OPEN");
    },

    // 영화 좋아요
    movielike() {
      const movieID = Number(this.$route.params.id);

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
    window.scrollTo(0, 0);

    const movieId = Number(this.$route.params.id);
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

    // 현재 로그인한 유저 영화 좋아요 여부 확인
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
  },
};
</script>

<style>
#app2 {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: black;
  padding: 60px 20px 20px 20px;
}

.upper-space {
  width: 100%;
  height: 50px;
}

.full_card_layout {
  font-family: "IBM Plex Sans KR", sans-serif;
  border: 2px solid white;
  border-radius: 15px;
  box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.1);
  color: #ffffff;
  padding: none;
  height: 70vw;
  background-color: rgb(20, 20, 21);
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
  margin: 0px 20px;
}

.movie-card-info {
  background: rgba(27, 26, 26, 0.823);
  opacity: 0.85;
  border-radius: 2% 0% 0% 6%;
  flex: 1;
  display: flex;
  border: thin solid #d4d4d468;
  height: 80%;
  flex-direction: column;
}

.movie-card-info-first {
  display: flex;
  flex-direction: row;
}

.movie-card-poster {
  width: 20vw;
  margin: 10px 0px 10px 10px;
  border-radius: 2%;
}

.movie-card-info-detail {
  margin: 40px;
  text-align: left;
}

.movie-card-info-overview {
  margin: 10px;
  padding: 20px;
  text-align: left;
}

.comment-button-space {
  display: flex;
  width: 100%;
}

.comment-button {
  border: 2px solid #171616e0;
  background-color: rgba(255, 255, 255, 0.635);
  padding: 8px 0px;
  width: 80%;
  text-align: center;
  border-radius: 10px;
  color: #050505;
  transition: all 100ms ease-in-out;
}

.comment-button:hover {
  background-color: rgba(255, 255, 255, 0.8);
  font-weight: 900;

  border-radius: 10px;
}

.comments-space {
  /* 왼쪽에 있는 영화 정보랑 높이 똑같게 맞추기 */
  flex: 1;
  border: 1px solid #d4d4d468;
  border-radius: 0% 2% 2% 0%;
  background: linear-gradient(
    186deg,
    darkviolet,
    rgb(6, 6, 230),
    #530754,
    #210891,
    #811ad0,
    #3e0328,
    #2814ed,
    #0e03a9,
    #f20193
  );
  background-size: 540% 540%;
  animation: gradient-animation 60s ease infinite;
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

@font-face {
  font-family: "KyoboHandwriting2020A";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2112@1.0/KyoboHandwriting2020A.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
.movie-card-comments {
  font-family: "KyoboHandwriting2020A";
  padding: 10px;
  text-align: left;
  border-radius: 0px 0px 10px 10px;
  height: 90%;
}

.movie-comment {
  padding-top: 50px;
  width: 500px;
}

/* Review PopUP */

.black-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
}

.white-bg {
  position: relative;
  width: 100%;
  height: 100%;
}

.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 2px 7px rgba(0, 0, 0, 0.3);
}
</style>
