<template>
  <div class="search-mini-card">
    <div class="mini-card">
      <div class="image-container">
        <img
          @click="toDetail"
          class="popup-poster search-popup-poster"
          :src="`https://image.tmdb.org/t/p/original/${movie.poster_path}`"
          :alt="movie.movie_id"
        />
        <p class="mini-card-title">{{ movie.title }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchMiniCard",
  props: {
    movie: Object,
  },
  computed: {
    searchMovieList() {
      return this.$store.state.SearchMovieList;
    },
    searchMovieListLength() {
      return this.$store.state.SearchMovieList.length;
    },
  },

  methods: {
    toDetail(event) {
      const movieID = Number(event.target.alt);
      this.$router.push({ name: "detail", params: { id: movieID } });
      this.$store.commit("CLOSE_POPUP");
    },
  },
};
</script>

<style>
.search-mini-card {
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.mini-card-title {
  font-weight: 600;
  padding-top: 10px;
  font-size: 15px;
}

.search-popup-poster {
  transition: all 500ms ease-in-out;
  width: 100%;
  height: auto;
}

.image-container:hover .mini-card-title {
  opacity: 1;
}

.image-container:hover .popup-poster {
  filter: brightness(0.3);
  cursor: pointer;
}

.image-container {
  position: relative;
}

.mini-card-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: 600;
  padding-top: 10px;
  font-size: 20px;
  color: white;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.mini-card-title:hover {
  cursor: pointer;
}
</style>
