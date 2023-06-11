<template>
  <div class="review-page">
    <div class="review-title">〈 {{ movie?.title }} 〉</div>
    <hr />
    <div class="detail-review-space">
      <ShowReview
        v-for="review in reviewList"
        :key="review.id"
        :review="review"
        @reviewDeleted="deleteReviewFromList"
      />
    </div>
  </div>
</template>

<script>
import ShowReview from "@/components/ReviewList/ShowReview.vue";

import axios from "axios";

export default {
  name: "ReviewView",
  components: {
    ShowReview,
  },
  data() {
    return {
      movie: null,
      reviewList: null,
    };
  },

  methods: {
    deleteReviewFromList(deletedReviewId) {
      this.reviewList = this.reviewList.filter(
        (review) => review.id !== deletedReviewId
      );
    },

    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  },

  created() {
    const movieId = Number(this.$route.params.id);
    const API_KEY = process.env.VUE_APP_TMDB_API_KEY;

    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieId}?api_key=${API_KEY}&language=ko-KR`,
    }).then((res) => {
      const movieData = res.data;
      this.movie = movieData;
    });

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/${movieId}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        this.reviewList = res.data;
        this.$nextTick(() => {
          this.scrollToTop(); // 스크롤 위치를 가장 상단으로 이동시킵니다.
        });
      })
      .catch((err) => {
        if (err.response && err.response.status === 404) {
          // 리뷰 데이터가 없을 경우 처리할 내용을 여기에 추가합니다.
          this.reviewList = []; // 리뷰 데이터가 없으므로 빈 배열로 설정합니다.
        } else {
          console.log(err);
        }
      });
  },
};
</script>

<style>
.review-page {
  font-family: "IBM Plex Sans KR", sans-serif;
  color: white;
  background-color: rgba(0, 0, 0, 0.88);
  height: 100%;
}

.review-title {
  padding-top: 100px;
  font-size: 30px;
}

.detail-review-space {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
