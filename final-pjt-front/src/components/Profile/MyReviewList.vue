<template>
  <div class="my-reviews">
    <img
      :src="`https://image.tmdb.org/t/p/original/${c_moviePosterPath}`"
      class="reco-poster"
      alt="리뷰 영화 포스터1"
    />

    <div class="review-movie-info">
      <h4 class="movie-title">
        <b> 〈 {{ c_movieTitle }} 〉 </b>
      </h4>
      <p class="my-review-short">"{{ review.title }}"</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "MyReviewList",
  props: {
    review: Object,
  },

  computed: {
    c_movieTitle() {
      return this.movieTitle;
    },
    c_movieOriginalTitle() {
      return this.movieOriginalTitle;
    },
    c_moviePosterPath() {
      return this.moviePosterPath;
    },
  },

  data() {
    return {
      movieTitle: null,
      movieOriginalTitle: null,
      moviePosterPath: null,
    };
  },

  created() {
    const API_KEY = process.env.VUE_APP_TMDB_API_KEY;
    const movieID = this.review.movie_id;
    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieID}?api_key=${API_KEY}&language=ko-KR`,
    }).then((res) => {
      this.movieTitle = res.data.title;
      this.movieOriginalTitle = res.data.original_title;
      this.moviePosterPath = res.data.poster_path;
    });
  },
};
</script>

<style>
.review-movie-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 85%;
}

.my-reviews {
  display: flex;
  border: 1px solid rgba(0, 0, 0, 0.3);
  width: 40vw;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
  align-items: center;
}

.movie-title {
  font-size: 15px;
}

.my-review-short {
  font-size: 20px;
  word-wrap: break-word;
  max-width: 30vw;
}
</style>
