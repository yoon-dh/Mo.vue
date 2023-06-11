import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";
import router from "../router";

const API_KEY = process.env.VUE_APP_TMDB_API_KEY;
const API_URL = "http://127.0.0.1:8000";

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [createPersistedState()],

  state: {
    // 현재 상영중 영화
    NowPlayingMovie: [],
    // 개봉 예정작
    UpcomingMovie: [],
    // 영화 클릭 시 팝업에 띄워줄 정보
    clickedPoster: null,
    clickedPosterDirector: null,
    clickedPosterActor: null,

    // 전체 Movie 받아와서 넣어둘 데이터
    MovieList: null,
    SearchMovieList: null,

    // ReviewPopup open&close
    isReviewPopup: false,

    // Topten ID 처리
    TopTenReviewID: null,

    // TOKEN
    token: null,

    // LOGIN POPUP open or close
    loginPopupOpen: false,

    // SIGNUP POPUP open or close
    signupPopupOpen: false,

    // get UserName & UserID after Login
    usernameANDuserid: null,
    username: null,
    userID: null,

    // Recommend MovieList
    recommendMovieList: null,
  },
  getters: {
    isLogin(state) {
      return state.token ? true : false;
    },
  },
  mutations: {
    GET_NOW_PLAYING(state, nowPlaying) {
      state.NowPlayingMovie = nowPlaying;
    },
    GET_UPCOMING(state, upcoming) {
      state.UpcomingMovie = upcoming;
    },
    POSTER_INFO(state, payload) {
      console.log(payload);
      state.clickedPoster = payload;
    },
    CLOSE_POPUP(state) {
      state.clickedPoster = null;
      state.SearchMovieList = null;
    },
    GET_DIRECTOR(state, payload) {
      state.clickedPosterDirector = payload;
    },
    GET_ACTORS(state, payload) {
      state.clickedPosterActor = payload;
    },
    GET_ALL_MOVIE(state, payload) {
      state.MovieList = payload;
    },
    GET_SEARCH_MOVIE(state, payload) {
      state.SearchMovieList = payload;
    },
    REVIEW_POPUP_OPEN(state) {
      state.isReviewPopup = true;
    },
    REVIEW_POPUP_CLOSE(state) {
      state.isReviewPopup = false;
      state.TopTenReviewID = null;
    },

    // top ten
    TOPTEN_REVIEW_ID(state, payload) {
      state.TopTenReviewID = payload;
    },

    // token
    SAVE_TOKEN(state, token) {
      state.token = token;
      router.push({ name: "home" }).catch(() => {}); // store/index.js $router 접근 불가 -> import를 해야함
    },

    LOGIN_POPUP_OPEN(state) {
      state.loginPopupOpen = true;
    },
    LOGIN_POPUP_CLOSE(state) {
      state.loginPopupOpen = false;
    },
    SIGNUP_POPUP_OPEN(state) {
      state.signupPopupOpen = true;
    },
    SIGNUP_POPUP_CLOSE(state) {
      state.signupPopupOpen = false;
    },

    // logout test
    LOGOUT_TOKEN(state) {
      state.token = null;
      state.username = null;
      state.userID = null;
    },

    // get username & user_id
    GET_USERNAME(state, payload) {
      state.usernameANDuserid = payload;
      state.username = payload.username;
      state.userID = payload.pk;
    },

    RECOMMEND_MOVIE_LIST(state, payload) {
      state.recommendMovieList = payload;
    },
  },
  actions: {
    // 현재 상영중 영화 받아오기
    getNowPlaying(context) {
      axios({
        method: "get",
        url: `https://api.themoviedb.org/3/movie/now_playing?api_key=${API_KEY}&language=ko-KR&page=1`,
      })
        .then((res) => {
          context.commit("GET_NOW_PLAYING", res.data.results);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    // 개봉 예정작 불러오기
    getUpcoming(context) {
      axios({
        method: "get",
        url: `https://api.themoviedb.org/3/movie/upcoming?api_key=${API_KEY}&language=ko-KR&page=1`,
      })
        .then((res) => {
          context.commit("GET_UPCOMING", res.data.results);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    // nowplaying, upcoming 클릭한 포스터 영화 데이터
    posterInfo(context, payload) {
      context.commit("POSTER_INFO", payload);
    },

    // 영화 감독, 출연진 데이터
    getDirectInfo(context, payload) {
      const movieID = payload.id;

      axios({
        method: "get",
        url: `https://api.themoviedb.org/3/movie/${movieID}/credits?api_key=${API_KEY}&language=en-US`,
      })
        .then((res) => {
          const cast = [res.data.cast[0], res.data.cast[1], res.data.cast[2]];
          context.commit("GET_ACTORS", cast);

          const crew = res.data.crew;
          for (let i = 0; i < crew.length - 1; i++) {
            if (crew[i].job === "Director") {
              context.commit("GET_DIRECTOR", crew[i].name);
              return;
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getAllMovie(context, payload) {
      context.commit("GET_ALL_MOVIE", payload);
    },

    getSearchMovie(context, payload) {
      context.commit("GET_SEARCH_MOVIE", payload);
    },

    // 회원가입(Sign-up)
    signUp(context, payload) {
      const username = payload.username;
      const password1 = payload.password1;
      const password2 = payload.password2;

      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: {
          username,
          password1,
          password2,
        },
      })
        .then((res) => {
          context.commit("SAVE_TOKEN", res.data.key);
          context.commit("SIGNUP_POPUP_CLOSE");
        })
        .then(() => {
          axios({
            method: "get",
            url: "http://127.0.0.1:8000/accounts/user/",
            headers: {
              Authorization: `Token ${this.state.token}`,
            },
          }).then((res) => {
            context.commit("GET_USERNAME", res.data);
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    // 로그인(Login)
    login(context, payload) {
      const username = payload.username;
      const password = payload.password;

      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          context.commit("SAVE_TOKEN", res.data.key);
          context.commit("LOGIN_POPUP_CLOSE");
        })
        .then(() => {
          axios({
            method: "get",
            url: "http://127.0.0.1:8000/accounts/user/",
            headers: {
              Authorization: `Token ${this.state.token}`,
            },
          }).then((res) => {
            context.commit("GET_USERNAME", res.data);
          });
        })
        .catch(() => {
          alert("일치하는 회원 정보가 없습니다!");
        });
    },

    // 로그아웃(Logout)
    logout(context) {
      const token = this.state.token;
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then(() => {
          context.commit("LOGOUT_TOKEN");
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  modules: {},
});
