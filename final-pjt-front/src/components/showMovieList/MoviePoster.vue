<template>
  <swiper-slide ref="swiperSlide">
    <img
      class="movie_poster"
      :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`"
      alt="poster"
      ref="posterImage"
    />
  </swiper-slide>
</template>

<script>
import { SwiperSlide } from "vue-awesome-swiper";

export default {
  name: "MoviePoster",
  props: {
    movie: Object,
  },
  components: {
    SwiperSlide,
  },
};
</script>

<style>
.movie_poster {
  width: 210px;
  aspect-ratio: 3/4;
  object-fit: cover;
  margin-right: 0px;
  transition: all 500ms ease-in-out;
  border-radius: 8px;
}

.movie_poster:hover {
  transform: scale(1.1);
  cursor: pointer;
}
</style>
