<template>
  <div class="popup-all" v-if="movie">
    <div>
      <img
        @click="closePopup"
        class="popup-close"
        src="@/assets/HomeView/Home/close.png"
        alt=""
      />
    </div>

    <div class="popup-main">
      <img
        class="popup-poster"
        :src="`https://image.tmdb.org/t/p/original/${movie?.poster_path}`"
        alt="poster"
      />
      <div class="popup-info">
        <p class="popup-title">
          {{ movie?.title }} ({{ movie?.original_title }})
        </p>
        <p>감독 : {{ movieDirector }}</p>
        <p>
          출연진 : {{ movieActors[0]?.name }}, {{ movieActors[1]?.name }},
          {{ movieActors[2]?.name }}
        </p>

        <p class="popup-content">{{ movieOverview }}</p>
        <button class="toDetail-btn" @click="toDetail">MORE</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MoviePopup",
  computed: {
    movie() {
      return this.$store.state.clickedPoster;
    },
    movieDirector() {
      return this.$store.state.clickedPosterDirector;
    },
    movieActors() {
      return this.$store.state.clickedPosterActor || [];
    },
    movieOverview() {
      if (!this.movie.overview) {
        return "현재 등록된 영화 정보가 없습니다.";
      }
      // return this.movie.overview;
      return this.movie ? this.movie.overview : "";
    },
  },
  methods: {
    closePopup() {
      this.$store.commit("CLOSE_POPUP");
    },
    toDetail() {
      const movieID = this.movie.id;
      this.$router.push({ name: "detail", params: { id: movieID } });
      this.$store.commit("CLOSE_POPUP");
    },
    // getActorName(index) {
    //   return this.movieActors && this.movieActors.length > index
    //     ? this.movieActors[index].name
    //     : "";
    // },
  },
};
</script>

<style>
.popup-poster {
  width: 250px;
  aspect-ratio: 3/4;
  object-fit: cover;
  border-radius: 8px;
}

.popup-all {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
}

.popup-main {
  display: flex;
  padding: 30px;
}

.popup-content {
  /* max-height: 6em;  */
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 6; /* 표시할 줄 수를 지정 */
  -webkit-box-orient: vertical;
  text-align: left;
}

.popup-info {
  padding: 20px;
  width: 40vw;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
}

.popup-title {
  font-size: 20px;
  font-weight: bold;
}

.popup-close {
  width: 30px;
  height: 30px;
  position: absolute;
  top: 15px;
  right: 15px;
}

.popup-close:hover {
  cursor: pointer;
}

.popup-close-hover {
  display: none;
  position: absolute;
  top: 15px;
  right: 15px;
  width: 30px;
  height: 30px;
  /* transition: opacity 0.3s; */
}

.popup-close-hover:hover {
  cursor: pointer;
}

.toDetail-btn {
  width: 92%;
  position: absolute;
  bottom: 0px;
  right: 20px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 8px;
  transition: all 500ms ease-in-out;
}

.toDetail-btn:hover {
  background: rgba(0, 0, 0, 0.7);
  cursor: pointer;
  color: white;
}
</style>
