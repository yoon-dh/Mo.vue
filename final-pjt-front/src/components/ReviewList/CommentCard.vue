<template>
  <div class="comment-space">
    <div>
      <b>{{ commentDetail?.username }} 님의 댓글</b>
      <p class="my-comment-detail">{{ commentDetail?.content }}</p>
      <p class="my-commnet-date">
        ⏱ {{ formatElapsedTime(commentDetail?.created_at) }} -
        <a class="comment_update">수정</a> |
        <a class="comment_delete" @click="deleteComment">삭제</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CommentCard",

  data() {
    return {
      commentDetail: null,
    };
  },

  props: {
    comment: Number,
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

    deleteComment() {
      const commentID = this.comment;

      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/reviews/comments/${commentID}/`,
        headers: {
          Authorization: `Token ${this.$store.state.token}`,
        },
      }).then(() => {
        // console.log(res);
        this.$emit("commentDeleted", commentID);
      });
    },
  },

  created() {
    const commentID = this.comment;

    axios({
      method: "get",
      url: `http://127.0.0.1:8000/reviews/comments/${commentID}/`,
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    })
      .then((res) => {
        this.commentDetail = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style>
.comment-space {
  padding: 10px 0px;
  display: flex;
  text-align: left;
  font-size: 17px;
}

.comment_update {
  text-decoration: none;
  color: grey;
  font-size: 13px;
  cursor: pointer;
}
.comment_delete {
  text-decoration: none;
  color: grey;
  font-size: 13px;
  cursor: pointer;
}
.my-comment-detail {
  margin: 10px;
  font-size: 16px;
  text-align: left;
}
.my-commnet-date {
  font-size: 13px;
  margin-left: 10px;
}
</style>
