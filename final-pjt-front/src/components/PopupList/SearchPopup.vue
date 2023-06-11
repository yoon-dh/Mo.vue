<template>
  <div class="popup-all">
    <div>
      <img
        @click="closePopup"
        class="popup-close"
        src="@/assets/HomeView/Home/close.png"
        alt=""
      />
    </div>

    <p class="search-message-bg">
      '{{ searchKeyword }}'의 검색 결과({{ SearchMovieList.length }})<br />
      <span class="search-message-sm">원하는 영화를 클릭하세요</span>
    </p>

    <div v-if="SearchMovieList.length === 0" class="search-message-empty">
      <p>검색 결과가 없습니다.</p>
    </div>
    <div v-else class="popup-main search-popup-main">
      <SearchMiniCard
        v-for="movie in SearchMovieList"
        :key="movie.id"
        :movie="movie"
      />
    </div>
  </div>
</template>

<script>
import SearchMiniCard from "@/components/showMovieList/SearchMiniCard.vue";

export default {
  name: "SearchPopup",
  components: {
    SearchMiniCard,
  },
  props: {
    searchKeyword: String,
  },
  computed: {
    SearchMovieList() {
      return this.$store.state.SearchMovieList;
    },
  },
  methods: {
    closePopup() {
      this.$store.commit("CLOSE_POPUP");
    },
  },
};
</script>

<style>
.search-message-bg {
  text-align: left;
  font-size: 20px;
  font-weight: bold;
  margin: 18px 0px 0px 50px;
}

.search-message-sm {
  font-size: 15px;
  font-weight: 400;
}

.search-popup-main {
  padding-bottom: 0px;
  padding-left: 20px;
  padding-top: 10px;
  display: flex;
  flex-wrap: wrap;
  max-height: 600px;
  overflow-y: auto;
}

.search-popup-main > .search-mini-card {
  width: calc(100% / 3);
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  align-items: flex-start;
}

.search-popup-main > .search-mini-card .popup-poster {
  width: 100%;
  aspect-ratio: 3/4;
  object-fit: cover;
  border-radius: 8px;
}

.search-popup-main > .search-mini-card .mini-card-title {
  width: 100%;
  font-weight: 600;
  padding-top: 10px;
  font-size: 20px;
  text-align: center;
}

.search-message-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 500px;
  height: 200px;
}
</style>
