<template>
  <div class="recommendview">
    <div class="recommend-upper"></div>
    <span class="stamp is-approved">Recommend</span>

    <img class="chain" src="@/assets/HomeView/popular/chain_final.png" alt="" />

    <div class="wrapper">
      <RecommendMovieCard
        class="card"
        v-for="movie in recommendMovieList"
        :key="movie"
        :top_recommend_movie="movie"
      />
    </div>
  </div>
</template>

<script>
import RecommendMovieCard from "@/components/showMovieList/RecommendMovieCard.vue";

export default {
  name: "RecommendView",
  components: {
    RecommendMovieCard,
  },
  computed: {
    recommendMovieList() {
      return this.$store.state.recommendMovieList;
    },
  },

  created() {
    window.scrollTo(0, 0);
  },
};
</script>

<style>
.stamp {
  position: fixed;
  top: 300px;
  left: 400px;
  font-size: 250px;
  transform: rotate(12deg);
  color: #555;

  font-weight: 700;
  border: 0.25rem solid #555;
  display: inline-block;
  padding: 0.25rem 1rem;
  text-transform: uppercase;
  border-radius: 1rem;
  font-family: "Courier";
  -webkit-mask-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/8399/grunge.png");
  -webkit-mask-size: 944px 604px;
  mix-blend-mode: multiply;
}

.is-approved {
  color: rgb(191, 5, 5);
  border: 1rem solid rgb(191, 5, 5);
  -webkit-mask-position: 13rem 6rem;
  transform: rotate(-14deg);
  border-radius: 0;
}
</style>
