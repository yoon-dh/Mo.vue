<template>
  <div class="">
    <div class="my-reviews">
      <img
        :src="`https://image.tmdb.org/t/p/original/${movie?.poster_path}`"
        class="reco-poster"
        alt="리뷰 영화 포스터1"
      />
      <div class="comment-movie-info">
        <b>〈 {{ movie?.title }} 〉</b>
        <p class="review-short">{{ review?.title }}</p>
      </div>
    </div>
    <div class="my-comment-short">
      <p class="turndownArrow">↪</p>
      <!-- <i class="fa fa-arrow-right" aria-hidden="true"></i> -->
      <p class="comment-content">{{ comment.content }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "MyCommentList",
  props: {
    comment: Object,
  },

  data() {
    return {
      review: null,
      movie: null,
    };
  },

  created() {
    const reviewID = this.comment.review;

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/review/${reviewID}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        this.review = res.data;
      })
      .then(() => {
        const movieID = this.review.movie_id;
        axios({
          method: "get",
          url: `http://127.0.0.1:8000/movies/${movieID}/`,
          headers: {
            Authorization: `Token ${this.$store.state.token}`,
          },
        }).then((res) => {
          this.movie = res.data;
        });
      });
  },
};
</script>

<style>
.my-reviews-first {
  display: flex;
}
.comment-movie-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 85%;
}
.review-short {
  word-wrap: break-word;
  max-width: 30vw;
}

.my-comment-short {
  display: flex;
}
.turndownArrow {
  font-size: 25px;
  margin: 0px 10px 0px 30px;
}
.comment-content {
  border: 2px solid rgba(1, 2, 20, 0.502);
  border-radius: 6px;
  font-weight: bold;
  padding: 11px;
}
</style>
