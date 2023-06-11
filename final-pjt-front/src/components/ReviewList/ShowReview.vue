<template>
  <div class="review-space">
    <div class="review-all">
      <div class="user_username_shortreview_score">
        <div class="shortreview">"{{ review.title }}" -</div>
        <div v-if="review.score === 5" class="score-star">★★★★★</div>
        <div v-else-if="review.score === 4" class="score-star">★★★★</div>
        <div v-else-if="review.score === 3" class="score-star">★★★</div>
        <div v-else-if="review.score === 2" class="score-star">★★</div>
        <div v-else class="score-star">★</div>
      </div>
      <div class="review">{{ review.content }}</div>
      <div class="create-at">
        ⏱ {{ formatElapsedTime(review.created_at) }}
        <a
          v-if="nowUser === review.username"
          class="delete-btn"
          @click="deleteReview"
        >
          - 삭제</a
        >
      </div>
      <div class="like_and_howmany_likes">
        <div class="like_and_howmany_likes_left">
          <button class="thumb-button" v-if="!review_liked" @click="reviewlike">
            <i class="fa fa-thumbs-up" aria-hidden="true"></i> Like
          </button>
          <button class="thumb-button-liked" v-else @click="reviewlike">
            <i class="fa fa-thumbs-up" aria-hidden="true"></i> Like
          </button>

          <p class="howmany_likes" v-if="review_liked_count == 1">
            {{ nowUser }}님이 좋아합니다.
          </p>
          <p class="howmany_likes" v-else-if="review_liked_count > 1">
            {{ nowUser }}님 외 {{ review_liked_count - 1 }}명이 좋아합니다.
          </p>
        </div>
        <p class="review-writer">
          <i>written by {{ review.username }}</i>
        </p>
      </div>
      <div class="hr"></div>

      <!-- comment List -->
      <!-- TODO:댓글 쓰자마자 바로 화면 변하게 하기 -->
      <CommentCard
        v-for="comment in reviewCommentSet"
        :key="comment.id"
        :comment="comment"
        @commentDeleted="removeComment(comment.id)"
      />

      <!-- comment -->
      <div class="form-floating">
        <p class="comment-alert">아래 댓글을 작성 해 주세요.</p>
        <textarea
          id="floatingTextarea"
          placeholder="Leave a comment here"
          type="text"
          class="form-control"
          v-model="commentContent"
        >
        </textarea>

        <button @click="createComment" class="comment-submit">SUBMIT</button>
      </div>
    </div>
  </div>
</template>

<script>
import CommentCard from "@/components/ReviewList/CommentCard.vue";

import axios from "axios";

export default {
  name: "ShowReview",

  components: {
    CommentCard,
  },

  data() {
    return {
      commentContent: null,
      review_user: null,
      review_liked: null,
      review_liked_count: null,
    };
  },

  computed: {
    reviewCommentSet() {
      return this.review.comment_set;
    },

    nowUser() {
      return this.$store.state.username;
    },
  },

  props: {
    review: Object,
  },

  methods: {
    formatElapsedTime(dateTime) {
      const currentTime = new Date();
      const elapsedMilliseconds = currentTime - new Date(dateTime);
      const elapsedMinutes = Math.floor(elapsedMilliseconds / 1000 / 60);

      if (elapsedMinutes < 1) {
        return "방금 전";
      } else if (elapsedMinutes < 60) {
        return `${elapsedMinutes}분 전`;
      } else if (elapsedMinutes < 1440) {
        const elapsedHours = Math.floor(elapsedMinutes / 60);
        return `${elapsedHours}시간 전`;
      } else {
        const elapsedDays = Math.floor(elapsedMinutes / 1440);
        return `${elapsedDays}일 전`;
      }
    },

    deleteReview() {
      const reviewID = this.review.id;
      console.log(typeof this.review.id);
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/reviews/${reviewID}/update_or_delete/`,
      })
        .then((res) => {
          console.log(res);
          this.$emit("reviewDeleted", this.review.id);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    createComment() {
      const reviewID = this.review.id;

      axios({
        method: "post",
        url: `http://127.0.0.1:8000/reviews/${reviewID}/comments/`,
        data: {
          content: this.commentContent,
        },
        headers: {
          Authorization: `Token ${this.$store.state.token}`,
        },
      }).then((res) => {
        console.log(res.data);
        this.commentContent = null;

        window.location.reload();
      });
    },

    removeComment(commentID) {
      const index = this.reviewCommentSet.findIndex(
        (comment) => comment.id === commentID
      );
      if (index !== -1) {
        this.reviewCommentSet.splice(index, 1);
      }
    },

    reviewlike() {
      const reviewID = this.review.id;

      axios({
        method: "post",
        url: `http://127.0.0.1:8000/reviews/${reviewID}/reviewlikes/`,
        headers: {
          Authorization: `Token ${this.$store.state.token}`,
        },
      }).then((res) => {
        this.review_liked = res.data.liked;
        this.review_liked_count = res.data.like_count;
      });
    },
  },

  created() {
    this.review_liked_count = this.review.like_users.length;

    const reviewId = this.review.id;
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/review/${reviewId}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    }).then((res) => {
      const reviewLikedUser = res.data.like_users;
      const loginUser = this.$store.state.userID;

      for (let i = 0; i < reviewLikedUser.length; i++) {
        if (reviewLikedUser[i] === loginUser) {
          this.review_liked = true;
          return;
        }
      }
      this.review_liked = false;
    });
  },
};
</script>

<style>
.review-space {
  margin-bottom: 20px;
  width: 100%;
}

.review-all {
  padding: 30px 30px 5px 30px;
  background-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 2px 7px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  color: black;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-left: 5vw;
  width: 90%;
}

.user_username_shortreview_score {
  display: flex;
  align-items: center;
}

.user-image {
  width: 40px;
  height: 40px;
  border-radius: 50px;
  margin-right: 10px;
}
.user_username {
  display: flex;
}

.user-name {
  font-size: 20px;
  font-weight: 200;
  font-weight: bold;
  width: 50px;
  flex: 0.08;
}

.review {
  padding: 30px 0px;
  text-align: left;
}

.shortreview {
  font-size: 20px;
  font-weight: 700;
  display: flex;
  text-align: left;
  margin-right: 10px;
}

.hr {
  width: 100%;
  height: 1px;
  background-color: black;
  margin: 10px 0;
}

.comment-submit {
  width: 100%;
}

.update-btn {
  text-decoration: none;
  color: grey;
}

.delete-btn {
  text-decoration: none;
  color: grey;
}

.delete-btn:hover {
  cursor: pointer;
}
.like_and_howmany_likes {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.comment-alert {
  text-align: left;
  padding: 10 0px;
  margin: 0px;
}

.howmany_likes {
  margin: 15px 10px 0px;
}

.form-floating {
  width: 100%;
  padding-bottom: 20px;
}

#floatingTextarea {
  width: 100%;
}

.comment-submit {
  border-radius: 5px;
}
.comment-submit:hover {
  background-color: rgba(0, 0, 0, 0.747);
  color: #fafafa;
}

.like_and_howmany_likes_left {
  display: flex;
}

.review-writer {
  margin-bottom: 0px;
}

.thumb-button {
  width: 73px;
  height: 37px;
  margin-top: 10px;
  justify-content: center;
  display: block;
  color: #4d4c4cab;
  background: #ffffff81;
  border: 2px solid #4285f4;
  font-size: 1em;
  font-weight: bold;
  outline: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}
.thumb-button-liked {
  width: 73px;
  height: 37px;
  margin-top: 10px;
  justify-content: center;
  display: block;
  color: #fafafa;
  background: #4285f4;
  border: 2px solid #4285f4;
  font-size: 1em;
  font-weight: bold;
  outline: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}

.thumb-button:hover {
  color: #fafafa;
  background: #4285f4;
}

.score-star {
  color: rgb(214, 106, 130);
  font-size: 20px;
  font-weight: bold;
}
</style>
