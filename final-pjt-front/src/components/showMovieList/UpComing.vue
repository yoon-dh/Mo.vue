<template>
  <div class="show-movie-list-item">
    <p class="movie-list-item-title">Upcoming</p>
    <div class="movie-list-item-poster">
      <swiper class="swiper" :options="swiperOption" @click-slide="posterInfo">
        <MoviePoster
          v-for="movie in UpcomingMovie"
          :key="movie.id"
          :movie="movie"
        />
        <div class="swiper-button-prev left" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
      </swiper>
    </div>
  </div>
</template>

<script>
import { Swiper } from "vue-awesome-swiper";
import "swiper/css/swiper.css";

import MoviePoster from "@/components/showMovieList/MoviePoster.vue";
export default {
  name: "UpComing",
  components: {
    MoviePoster,
    Swiper,
  },
  props: {
    UpcomingMovie: Array,
  },
  computed: {
    swiperOption() {
      return {
        slidesPerView: 6,
        spaceBetween: 30,
        loop: true,
        autoplay: {
          delay: 3000,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      };
    },

    isLogin() {
      return this.$store.getters.isLogin;
    },
  },
  methods: {
    posterInfo(index, reallyIndex) {
      if (this.isLogin) {
        const clikedPoster = this.UpcomingMovie[reallyIndex];
        this.$store.dispatch("posterInfo", clikedPoster);
        this.$store.dispatch("getDirectInfo", clikedPoster);
      } else {
        this.$store.commit("LOGIN_POPUP_OPEN");
      }
    },
  },
};
</script>

<style>
.movie-list-item-title {
  font-size: 30px;
  text-align: left;
  padding: 10px;
  margin: 0px;
  margin-left: 15px;
}

.movie-list-item-poster {
  display: flex;
  justify-content: space-between;
}
</style>
