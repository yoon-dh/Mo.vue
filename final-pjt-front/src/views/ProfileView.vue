<template>
  <div class="Profile">
    <h2 class="profile-username">{{ username }}님의 프로필</h2>
    <div class="profilePage">
      <div class="profile-first">
        <h3 class="likemovie-title">Like Movie</h3>
        <div class="like-movie-list-item-poster">
          <swiper
            class="swiper user-swiper"
            :options="swiperOption"
            @click-slide="posterInfo"
          >
            <LikedMovieList
              v-for="movie in LikedMovieList"
              :key="movie.id"
              :movie="movie"
            />
          </swiper>
        </div>
      </div>

      <div class="profile-second">
        <div class="profile-my-review-list">
          <h3 class="profile-reco-title">My Reviews</h3>
          <MyReviewList
            v-for="review in userReview"
            :key="review.id"
            :review="review"
          />
        </div>

        <div class="profile-my-review-comment-list">
          <h3 class="profile-reco-title">My Comments</h3>
          <MyCommentList
            v-for="comment in userComment"
            :key="comment.id"
            :comment="comment"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Swiper } from "vue-awesome-swiper";
import "swiper/css/swiper.css";

import LikedMovieList from "@/components/Profile/LikedMovieList.vue";
import MyReviewList from "@/components/Profile/MyReviewList.vue";
import MyCommentList from "@/components/Profile/MyCommentList.vue";

import axios from "axios";
export default {
  name: "ProfileView",
  components: {
    LikedMovieList,
    MyReviewList,
    MyCommentList,
    Swiper,
  },

  computed: {
    swiperOption() {
      return {
        slidesPerView: 5,
        spaceBetween: 20,
        loop: true,
        autoplay: {
          delay: 5000,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      };
    },
  },

  data() {
    return {
      LikedMovieList: null,
      userID: this.$route.params.userID,
      username: this.$store.state.username,
      userReview: [],
      userComment: [],
    };
  },

  methods: {
    posterInfo(index, reallyIndex) {
      //   console.log(this.LikedMovieList[reallyIndex].movie_id);
      //   console.log(index, reallyIndex);
      this.$router.push({
        name: "detail",
        params: { id: this.LikedMovieList[reallyIndex].movie_id },
      });
    },
  },

  created() {
    axios({
      method: "get",
      url: "http://127.0.0.1:8000/movies/movielikes/",
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    }).then((res) => {
      //   console.log(res.data);
      this.LikedMovieList = res.data;
    });

    const userID = Number(this.$route.params.userID);

    axios({
      method: "get",
      url: "http://127.0.0.1:8000/reviews/review_all/",
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    }).then((res) => {
      const reviewALL = res.data;
      for (let i = 0; i < reviewALL.length; i++) {
        if (reviewALL[i].user === userID) {
          this.userReview.push(reviewALL[i]);
        }
      }
    });

    axios({
      method: "get",
      url: "http://127.0.0.1:8000/reviews/comments/",
      headers: {
        Authorization: `Token ${this.$store.state.token}`,
      },
    }).then((res) => {
      //   console.log(res.data);
      const commentALL = res.data;
      for (let i = 0; i < commentALL.length; i++) {
        if (commentALL[i].user === userID) {
          this.userComment.push(commentALL[i]);
          //   console.log(this.userComment);
        }
      }
    });
  },
};
</script>

<style>
.like-movie-list-item-poster {
  display: flex;
  justify-content: center;
  padding: 20px 5px;
  width: 80vw;
  border: 1px solid rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}

.Profile {
  font-family: "IBM Plex Sans KR", sans-serif;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding-top: 60px;
  background-color: rgba(0, 0, 0, 0.9);
}

.profile-username {
  color: white;
}

.profilePage {
  border: 2px solid white;
  border-radius: 20px;
  margin: 30px;
  background-color: rgba(255, 255, 255, 0.85);
}

.profile-first {
  display: flex;
  margin-top: 10px;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.profile-username {
  display: flex;
}

.profile-like-movie-list {
  display: flex;
  flex-direction: column;
}

.like-movies {
  display: flex;
}

.profile-my-review-list {
  flex: 1;
  padding: 20px;
  border-right: 1px solid #535353;
  height: 80%;
  display: flex;
  flex-direction: column;
  /* justify-content: flex-start; */
  align-items: center;
}
.reco-poster {
  width: 60px;
  height: 60px;
  border: 1px solid rgb(249, 249, 249);
  border-radius: 70px;
  margin-right: 10px;
}
.profile-second {
  display: flex;
}

.profile-my-review-comment-list {
  flex: 1;
  margin: 20px;
  display: flex;
  flex-direction: column;
}

.movie-title {
  margin-right: 10px;
}
</style>
