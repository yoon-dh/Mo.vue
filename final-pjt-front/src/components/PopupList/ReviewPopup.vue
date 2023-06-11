<template>
  <div class="popup-all">
    <div class="review-popup-top">
      <img
        @click="closePopup"
        class="popup-close"
        src="@/assets/HomeView/Home/close.png"
        alt=""
      />
    </div>

    <div class="review-popupp-main">
      <form class="review-form" @submit.prevent="createReview">
        <div>
          <label for="movie-score">평점 : </label>
          <input type="number" min="1" max="5" v-model="score" />
        </div>
        <br />
        <div>
          <input
            id="short-review"
            placeholder="한줄평을 작성 해 주세요."
            type="text"
            size="50"
            maxlength="100"
            v-model="shortrReview"
          />
        </div>
        <br />
        <div>
          <textarea
            id="review-space"
            placeholder="영화에 대한 리뷰를 자유롭게 작성 해 주세요."
            type="text"
            rows="5"
            cols="60"
            v-model="review"
          />
        </div>
        <br />
        <input class="write-review-button" type="submit" value="Wrtie Review" />
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReviewPopup",
  data() {
    return {
      score: null,
      shortrReview: null,
      review: null,
    };
  },

  props: {
    movieID: Number,
  },

  computed: {
    RealReviewID() {
      return this.$store.state.TopTenReviewID;
    },
  },

  methods: {
    closePopup() {
      this.$store.commit("REVIEW_POPUP_CLOSE");
    },

    createReview() {
      if (this.RealReviewID === null) {
        if (this.score && this.shortrReview && this.review) {
          axios({
            method: "post",
            url: `http://127.0.0.1:8000/reviews/${this.movieID}/`,
            data: {
              title: this.shortrReview,
              content: this.review,
              movie_id: this.movieID,
              score: this.score,
            },
            headers: {
              Authorization: `Token ${this.$store.state.token}`,
            },
          })
            .then(() => {
              this.closePopup();
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          alert("리뷰를 모두 작성 해 주세요!");
        }
      } else {
        if (this.score && this.shortrReview && this.review) {
          axios({
            method: "post",
            url: `http://127.0.0.1:8000/reviews/${this.RealReviewID}/`,
            data: {
              title: this.shortrReview,
              content: this.review,
              movie_id: this.RealReviewID,
              score: this.score,
            },
            headers: {
              Authorization: `Token ${this.$store.state.token}`,
            },
          })
            .then(() => {
              this.closePopup();
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          alert("채워주세요.");
        }
      }
    },
  },
};
</script>

<style>
.review-popup-top {
  color: black;
}
.review-popup-title {
  margin-top: 20px;
  font-weight: bold;
  font-size: 20px;
}
.review-form {
  display: flex;
  color: black;
  flex-direction: column;
  padding: 30px;
  align-items: flex-start;
}
.write-review-button {
  width: 60%;
  height: 40px;
  margin: auto;
  justify-content: center;
  display: block;
  color: #fff;
  background: #080808d6;
  border: 1px solid white;
  font-size: 1em;
  font-weight: bold;
  outline: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}
.write-review-button:hover {
  background: #ffffffea;
  color: rgb(0, 0, 0);
  border: 2px solid #080808d6;
}
</style>
