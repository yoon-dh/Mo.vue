import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import MovieCard from "../views/MovieCard.vue";
import ReviewView from "../views/ReviewView.vue";
import TopRatedView from "../views/TopRatedView.vue";
import ProfileView from "../views/ProfileView.vue";
import RecommendView from "../views/RecommendView.vue";
import NotFound404 from "../views/NotFound404.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },

  {
    path: "/detail/:id",
    name: "detail",
    component: MovieCard,
  },

  {
    path: "/review/:id",
    name: "review",
    component: ReviewView,
  },

  {
    path: "/profile/:userID",
    name: "profile",
    component: ProfileView,
  },

  // TOP RATED PAGE
  {
    path: "/toprated",
    name: "toprated",
    component: TopRatedView,
  },

  // RECOMMEND PAGE
  {
    path: "/recommend",
    name: "recommend",
    component: RecommendView,
  },

  // 404
  {
    path: "/404",
    name: "NotFound404",
    component: NotFound404,
  },

  {
    path: "*",
    redirect: "/404",
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
