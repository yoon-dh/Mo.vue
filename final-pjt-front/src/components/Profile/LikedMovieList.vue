<template>
  <swiper-slide class="like-movies">
    <div class="user-image-container">
      <img
        class="like-movie-poster"
        :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`"
        alt=""
      />
      <p class="user-mini-card-title">{{ movie.title }}</p>
    </div>
  </swiper-slide>

  <!-- <div>LIKED MOVIE LIST</div> -->
</template>

<script>
import { SwiperSlide } from "vue-awesome-swiper";

export default {
  name: "LikedMovieList",
  props: {
    movie: Object,
  },
  components: {
    SwiperSlide,
  },
  methods: {},
};
</script>

<style>
.like-movie-poster {
  width: 180px;
  aspect-ratio: 3/4;
  object-fit: cover;
  margin-right: 0px;
  border-radius: 8px;
}

.like-movie-poster:hover {
  opacity: 1;
}

.user-image-container {
  position: relative;
}

.user-mini-card-title {
  font-weight: 600;
  padding-top: 10px;
  font-size: 15px;
}

.user-mini-card-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: 600;
  padding-top: 10px;
  font-size: 15px;
  color: white;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.user-image-container:hover .user-mini-card-title {
  opacity: 1;
}

.user-image-container:hover .like-movie-poster {
  filter: brightness(0.3);
  cursor: pointer;
}

.user-mini-card-title:hover {
  cursor: pointer;
}
</style>
