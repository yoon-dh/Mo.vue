<template>
  <div class="topratedview">
    <img class="chain" src="@/assets/HomeView/popular/chain_final.png" alt="" />
    <span class="stamp is-approved">TopRated</span>

    <div class="wrapper">
      <TopTenMovieCard
        class="card"
        v-for="movie in topratedmovieList"
        :key="movie.id"
        :top_recommend_movie="movie"
        :movieIDD="movie.id"
      />
    </div>
  </div>
</template>

<script>
import TopTenMovieCard from "@/components/showMovieList/TopTenMovieCard.vue";

import axios from "axios";
export default {
  name: "TopRatedView",

  components: {
    TopTenMovieCard,
  },

  data() {
    return {
      topratedmovieList: [],
    };
  },

  created() {
    window.scrollTo(0, 0);

    const API_KEY = process.env.VUE_APP_TMDB_API_KEY;

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/top_rated?api_key=${API_KEY}&language=ko-KR&page=1`,
    }).then((res) => {
      for (let i = 0; i < 10; i++) {
        this.topratedmovieList.push(res.data.results[i]);
      }
    });
  },
};
</script>

<style>
.top-rated-upper {
  height: 100px;
  background-color: black;
}

.wrapper {
  margin: 10 auto;
}

.card {
  border: 2px solid black;
  border-radius: 10px;
  box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.1);
  color: #ffffff;
  padding: 40px;
  height: 70vw;
  position: sticky;
}

.card:nth-child(1n) {
  top: 65px;
  background-color: rgba(0, 0, 0);
}

.card:nth-child(2n) {
  top: 70px;
}

.card:nth-child(3n) {
  top: 75px;
}

.card:nth-child(4n) {
  top: 80px;
}

.card:nth-child(5n) {
  top: 85px;
}

.card:nth-child(6n) {
  top: 90px;
}

.card:nth-child(7n) {
  top: 95px;
}

.card:nth-child(8n) {
  top: 100px;
}
.card:nth-child(9n) {
  top: 105px;
}
.card:nth-child(10n) {
  top: 110px;
}

.chain {
  z-index: 1000;
}

.stamp {
  position: fixed;
  cursor: default;
  top: 100px;
  left: 200px;
  font-size: 150px;
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
  color: rgb(191, 5, 5);
  border: 1rem solid rgb(191, 5, 5);
  -webkit-mask-position: 13rem 6rem;
  transform: rotate(-14deg);
  border-radius: 0;
  animation: fade--in 1.5s ease-in;
}
@keyframes fade--in {
  0% {
    opacity: 0;
    /* transform: translateY(20px); */
  }
  100% {
    opacity: 0;
    transform: rotate(-14deg);
  }
}
</style>
