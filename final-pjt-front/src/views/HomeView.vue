<template>
  <div class="home">
    <!-- home-first-page(search) -->
    <img
      class="background-img"
      src="@/assets/HomeView/Home/1_background_spiderman.png"
      data-aos="fade-zoom-in"
      data-aos-easing="ease-in-back"
      data-aos-delay="100"
      data-aos-offset="0"
      data-aos-duration="2000"
    />
    <img
      class="black-image_under"
      src="@/assets/HomeView/Home/blackimage.png"
      alt=""
    />
    <img
      class="black-image_under2"
      src="@/assets/HomeView/Home/blackimage.png"
      alt=""
    />
    <img
      class="black-image"
      draggable="false"
      src="@/assets/HomeView/Home/blackimage.png"
      alt=""
    />
    <section class="home-first-page">
      <div class="home-first-page-section">
        <div
          class="home-first-section-big"
          data-aos="fade-up"
          data-aos-delay="2100"
          data-aos-duration="1000"
        >
          Movies are experiences, Not just watching
        </div>
        <div
          class="home-first-section-small"
          data-aos="fade-up"
          data-aos-delay="2100"
          data-aos-duration="1200"
        >
          You can experience it with us now
        </div>
        <!-- search-bar -->
        <form
          @submit.prevent="searchMovie"
          id="search-section"
          data-aos="fade-zoom-in"
          data-aos-easing="ease-in-back"
          data-aos-delay="2900"
          data-aos-offset="0"
          data-aos-duration="500"
        >
          <input
            id="search-bar"
            class="form-control me-2"
            type="search"
            placeholder="원하는 영화를 검색하세요"
            aria-label="Search"
            v-model.trim="searchKeyword"
            autocomplete="off"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </section>

    <!-- show-movie-list -->

    <section
      class="show-movie-list"
      data-aos="fade-zoom-in"
      data-aos-easing="ease-in-back"
      data-aos-delay="100"
      data-aos-offset="0"
      data-aos-duration="2000"
    >
      <NowPlaying :NowPlayingMovie="NowPlayingMovie" />

      <UpComing :UpcomingMovie="UpcomingMovie" />
    </section>

    <!-- home-second-page(popular) -->

    <section id="recommend" class="home-second-page">
      <div class="second-page-left">
        <div
          v-if="username"
          class="second-page-left-big"
          data-aos="fade-up"
          data-aos-duration="1000"
        >
          {{ username }}님을 위한 컨텐츠
        </div>
        <div
          v-else
          class="second-page-left-big"
          data-aos="fade-up"
          data-aos-duration="1000"
        >
          회원님을 위한 컨텐츠
        </div>
        <div
          class="second-page-left-small"
          data-aos="fade-up"
          data-aos-duration="1000"
        >
          선호하는 장르를 기반으로 좋아할 만한 작품만 모아봤어요.
        </div>
        <button
          class="recommend-btn"
          data-aos="fade-up"
          data-aos-duration="1000"
          @click="toRecommend"
        >
          show more
        </button>
      </div>
      <div class="second-page-right">
        <img
          data-aos="fade-up"
          data-aos-duration="1000"
          src="@/assets/HomeView/recommend/3-recommend-1.png"
          alt="image"
        />
      </div>
    </section>

    <!-- home-third-page(recommend) -->

    <section id="popular" class="home-third-page">
      <div class="third-page-left">
        <div
          class="third-page-left-big"
          data-aos="fade-up"
          data-aos-duration="1000"
        >
          평단의 찬사를 받은 시리즈
        </div>
        <div
          class="third-page-left-small"
          data-aos="fade-up"
          data-aos-duration="1000"
        >
          최대 Ultra HD 4K 해상도로 생생한 감동을 느껴보세요.
        </div>
        <button
          class="popular-btn"
          data-aos="fade-up"
          data-aos-duration="1000"
          @click="toPopular"
        >
          show more
        </button>
      </div>
      <div class="third-page-right">
        <img
          data-aos="fade-up"
          data-aos-duration="1000"
          src="@/assets/HomeView/popular/2-popular-1.png"
          alt="image"
        />
      </div>
    </section>

    <!-- go to top button -->
    <section class="top-btn-section">
      <button class="top-btn">TOP</button>
    </section>

    <!-- POP-UP Open & Close -->

    <div class="black-bg" v-if="isClickMovie !== null">
      <div class="white-bg">
        <MoviePopup class="popup" />
      </div>
    </div>

    <!-- Search POP-UP Open & Close -->
    <div class="black-bg" v-if="isSearchMovie !== null">
      <div class="white-bg">
        <SearchPopup class="popup" :searchKeyword="searchKeyword" />
      </div>
    </div>

    <!-- Login POP-UP Open & Close -->
    <div class="black-bg" v-if="isLoginPopupOpen">
      <div class="white-bg">
        <LoginPopup class="black-popup" />
      </div>
    </div>

    <!-- SignUp POP-UP Open & Close -->
    <div class="black-bg" v-if="isSignupPopupOpen">
      <div class="white-bg">
        <SignupPopup class="black-popup" />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import NowPlaying from "@/components/showMovieList/NowPlaying.vue";
import UpComing from "@/components/showMovieList/UpComing.vue";
import MoviePopup from "@/components/PopupList/MoviePopup.vue";
import SearchPopup from "@/components/PopupList/SearchPopup.vue";
import LoginPopup from "@/components/PopupList/LoginPopup.vue";
import SignupPopup from "@/components/PopupList/SignupPopup.vue";

import axios from "axios";

export default {
  name: "HomeView",
  components: {
    NowPlaying,
    UpComing,
    MoviePopup,
    SearchPopup,
    LoginPopup,
    SignupPopup,
  },
  data() {
    return {
      isScrolled: false,
      movieAll: null,
      searchKeyword: null,
    };
  },

  computed: {
    NowPlayingMovie() {
      return this.$store.state.NowPlayingMovie;
    },
    UpcomingMovie() {
      return this.$store.state.UpcomingMovie;
    },
    isClickMovie() {
      return this.$store.state.clickedPoster;
    },
    isSearchMovie() {
      return this.$store.state.SearchMovieList;
    },

    // 로그인 여부 판단
    isLogin() {
      return this.$store.getters.isLogin;
    },

    isLoginPopupOpen() {
      return this.$store.state.loginPopupOpen;
    },

    isSignupPopupOpen() {
      return this.$store.state.signupPopupOpen;
    },

    username() {
      return this.$store.state.username;
    },
  },

  methods: {
    getNowPlaying() {
      this.$store.dispatch("getNowPlaying");
    },
    getUpcoming() {
      this.$store.dispatch("getUpcoming");
    },
    closePopup() {
      this.$store.commit("CLOSE_POPUP");
    },
    searchMovie() {
      if (this.isLogin) {
        const keyword = this.searchKeyword;
        if (!keyword) {
          alert("찾고싶은 영화를 입력하세요!");
          return;
        }
        const MovieAll = this.$store.state.MovieList;
        const findMovieList = [];

        for (let i = 0; i < MovieAll.length; i++) {
          if (MovieAll[i].title.includes(keyword)) {
            findMovieList.push(MovieAll[i]);
          }
        }

        this.$store.dispatch("getSearchMovie", findMovieList);
      } else {
        this.$store.commit("LOGIN_POPUP_OPEN");
      }
    },

    toPopular() {
      if (this.isLogin) {
        this.$router.push({ name: "toprated" });
      } else {
        this.$store.commit("LOGIN_POPUP_OPEN");
      }
    },

    toRecommend() {
      if (this.isLogin) {
        this.$router.push({ name: "recommend" });
      } else {
        this.$store.commit("LOGIN_POPUP_OPEN");
      }
    },
  },

  created() {
    this.getNowPlaying();
    this.getUpcoming();

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/movies/`,
    })
      .then((res) => {
        this.$store.dispatch("getAllMovie", res.data);
        this.movieAll = res.data;
      })
      .catch((err) => {
        console.log(err);
      });

    const userID = this.$store.state.userID;

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/movies/recommend/${userID}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        this.$store.commit("RECOMMEND_MOVIE_LIST", res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  },

  mounted() {
    document.addEventListener("DOMContentLoaded", () => {
      const backgroundBlack = document.querySelector(".black-image");
      const backgroundBlackHeight =
        backgroundBlack.getBoundingClientRect().height;

      document.addEventListener("scroll", () => {
        backgroundBlack.style.opacity = window.scrollY / backgroundBlackHeight;
      });

      const topBtn = document.querySelector(".top-btn");
      topBtn.addEventListener("click", (event) => {
        console.log(event);
        scrollIntoView(".home");
      });
    });
  },
};

//Make home slowly gade to transparent as the window scrolls down
// arrow-up button

function scrollIntoView(selector) {
  const scrollTo = document.querySelector(selector);
  scrollTo.scrollIntoView({ behavior: "smooth" });
}
</script>

<style>
/* first-page */

.home-first-page {
  font-family: "Merriweather", serif;
  height: 65vw;
}

.background-img {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 65vw;
  opacity: 0.92;
}

.black-image {
  z-index: 1;
  position: absolute;
  width: 100%;
  height: 65vw;
  top: 0px;
  left: 0px;
  opacity: 0;
}

.black-image_under {
  z-index: -1;
  width: 100%;
  height: 65vw;
  position: absolute;
  top: 0px;
  left: 0px;
}

.black-image_under2 {
  width: 100%;
  height: 60vw;
  position: absolute;
  top: 65vw;
  left: 0px;
}

.home-first-page-section {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
}

.home-first-section-big {
  font-size: 42px;
  margin-bottom: 15px;
}

.home-first-section-small {
  font-size: 25px;
  margin-bottom: 25px;
}

/* search-bar */

#search-section {
  display: flex;
  justify-content: center;
  width: 100%;
  z-index: 3;
}

#search-bar {
  font-family: "IBM Plex Sans KR", sans-serif;
  width: 40%;
}

/* show-movie-list */

.show-movie-list {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-size: 100px;
  height: 55vw;
  background-color: black;
  color: white;
}

/* home-second-page(popular) */

.home-second-page {
  height: 80vh;
  background-color: black;
  color: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.second-page-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.second-page-left-big {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-size: 35px;
  padding: 10px;
}

.second-page-left-small {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-size: 20px;
  padding-bottom: 50px;
}

.popular-btn {
  font-family: "IBM Plex Sans KR", sans-serif;
  background-color: rgb(245, 191, 79);
  border: none;
  border-radius: 40px;
  color: white;
  width: 50%;
  height: 50px;
  opacity: 0.7;
  font-size: 25px;
}

.popular-btn:hover {
  cursor: pointer;
  opacity: 1;
}

/* home-third-page(recommed) */

.home-third-page {
  height: 80vh;
  background-color: black;
  color: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.third-page-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.third-page-left-big {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-size: 35px;
  padding: 10px;
}

.third-page-left-small {
  font-family: "IBM Plex Sans KR", sans-serif;
  font-size: 20px;
  padding-bottom: 50px;
}

.recommend-btn {
  font-family: "IBM Plex Sans KR", sans-serif;
  background-color: rgb(245, 191, 79);
  border: none;
  border-radius: 40px;
  color: white;
  width: 50%;
  height: 50px;
  opacity: 0.1;
  font-size: 25px;
}

.recommend-btn:hover {
  cursor: pointer;
  opacity: 1;
}

/* top-btn */

.top-btn-section {
  background-color: black;
  padding-bottom: 30px;
}

.top-btn {
  font-family: "IBM Plex Sans KR", sans-serif;
  background-color: transparent;
  width: 80px;
  color: grey;
  border: 1px solid transparent;
  padding: 12px 18px;
}

.top-btn:hover {
  color: white;
  border: 1px solid white;
  border-radius: 10px;
}

/* POP-UP Window */

.black-bg {
  font-family: "IBM Plex Sans KR", sans-serif;
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

.black-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.387);
}
</style>
