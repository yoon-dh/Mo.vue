<template>
  <swiper-slide class="shortreview-show">
    <div
      v-for="review in shortreview"
      :key="review.id"
      :class="getSlideClass(review)"
    >
      {{ review.title }}
      <div v-if="review.score === 5" class="moviecard-score-star">- ★★★★★</div>
      <div v-else-if="review.score === 4" class="moviecard-score-star">
        -★★★★
      </div>
      <div v-else-if="review.score === 3" class="moviecard-score-star">
        -★★★
      </div>
      <div v-else-if="review.score === 2" class="moviecard-score-star">-★★</div>
      <div v-else class="moviecard-score-star">-★</div>
    </div>
  </swiper-slide>
</template>

<script>
import { SwiperSlide } from "vue-awesome-swiper";

export default {
  name: "MovieShortReview",
  components: {
    SwiperSlide,
  },
  props: {
    shortreview: Array,
  },

  methods: {
    getSlideClass(review) {
      const reviewList = this.shortreview;

      if (reviewList.indexOf(review) === 0) {
        return "first-review";
      } else if (reviewList.indexOf(review) === 1) {
        return "second-review";
      } else if (reviewList.indexOf(review) === 2) {
        return "third-review";
      } else {
        return "fourth-review";
      }
    },
  },
};
</script>

<style>
.shortreview-show {
  color: white;
  margin-bottom: 30px;
}

.one-short-review {
  font-weight: bold;
  font-size: 30px;
  margin-bottom: 50px;
}

.first-review {
  font-weight: bold;
  font-size: 22px;
  margin-bottom: 45px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  animation: fadein 3s ease-in-out;
}
@keyframes fadein {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 0.6;
    transform: none;
  }
}

.second-review {
  font-weight: bold;
  font-size: 22px;
  margin-bottom: 45px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  animation: fadein 6s ease-in-out;
}
@keyframes fadein {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 0.6;
    transform: none;
  }
}

.third-review {
  font-weight: bold;
  font-size: 22px;
  margin-bottom: 45px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  animation: fadein 9s ease-in-out;
}
@keyframes fadein {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 0.6;
    transform: none;
  }
}

.fourth-review {
  font-weight: bold;
  font-size: 22px;
  margin-bottom: 45px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  animation: fadein 12s ease-in-out;
}
@keyframes fadein {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 0.6;
    transform: none;
  }
}
.moviecard-score-star {
  color: rgb(243, 237, 74);
  font-size: 20px;
  font-weight: bold;
}
</style>
