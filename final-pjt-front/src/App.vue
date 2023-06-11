<template>
  <div id="app">
    <!-- nav-bar -->
    <nav
      class="nav-bar"
      data-aos="fade-zoom-in"
      data-aos-easing="ease-in-back"
      data-aos-delay="100"
      data-aos-offset="0"
      data-aos-duration="2000"
    >
      <div class="nav-left">
        <a class="nav-bar-title" @click="toHome">
          <img class="nav-bar-logo" src="./assets/mo.vue_logo.png" alt="Logo" />
          <div>Mo.vue</div>
        </a>
      </div>
      <div class="nav-bar-btn-list">
        <button @click="toRecommend" class="nav-bar-btn" data-link="#recommend">
          Recommend
        </button>
        <button @click="toPopulat" class="nav-bar-btn" data-link="#popular">
          Popular
        </button>
        <button v-if="!isLogin" @click="toLogin" class="nav-bar-btn">
          Login
        </button>
        <div v-else>
          <button @click="toProfile" class="nav-bar-btn">Profile</button>
          <button @click="logout" class="nav-bar-btn">Logout</button>
        </div>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script>
// Make navbar transparent when it is on top
export default {
  name: "App",

  computed: {
    isLogin() {
      return this.$store.getters.isLogin;
    },

    userID() {
      return this.$store.state.userID;
    },
  },
  methods: {
    toHome() {
      const currentRoute = this.$router.currentRoute;
      if (currentRoute.name !== "home") {
        this.$router.push({ name: "home" });
      }
    },

    toLogin() {
      this.$store.commit("LOGIN_POPUP_OPEN");
    },

    logout() {
      this.$store.dispatch("logout");
      this.$router.push({ name: "home" }).catch(() => {});
    },

    toProfile() {
      const currentRoute = this.$router.currentRoute;
      if (currentRoute.name !== "profile") {
        this.$router.push({ name: "profile", params: { userID: this.userID } });
      }
    },

    toRecommend() {
      console.log("aaaa");
      const currentRoute = this.$router.currentRoute;
      if (currentRoute.name === "home") {
        const target = event.target;
        const link = target.dataset.link;
        if (link == null) {
          return;
        }
        scrollIntoView(link);
        return;
      } else if (currentRoute.name === "recommend") {
        return;
      } else {
        this.$router.push({ name: "recommend" });
      }
    },

    toPopulat() {
      console.log("bbbb");
      const currentRoute = this.$router.currentRoute;
      if (currentRoute.name === "home") {
        const target = event.target;
        const link = target.dataset.link;
        if (link == null) {
          return;
        }
        scrollIntoView(link);
        return;
      } else if (currentRoute.name === "toprated") {
        return;
      } else {
        this.$router.push({ name: "toprated" });
      }
    },
  },
};

document.addEventListener("DOMContentLoaded", () => {
  const navbar = document.querySelector("nav");
  const navbarHeight = navbar.getBoundingClientRect().height;

  document.addEventListener("scroll", () => {
    if (window.scrollY > navbarHeight) {
      navbar.classList.add("nav-bar--dark");
    } else {
      navbar.classList.remove("nav-bar--dark");
    }
  });

  // navbar.addEventListener("click", (event) => {
  //   const target = event.target;
  //   const link = target.dataset.link;
  //   if (link == null) {
  //     return;
  //   }
  //   scrollIntoView(link);
  // });
});

// Handle scrolling when tapping on the navbar menu

function scrollIntoView(selector) {
  const scrollTo = document.querySelector(selector);
  scrollTo.scrollIntoView({ behavior: "smooth" });
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

/* nav-bar */

.nav-bar {
  font-family: "Merriweather", serif;
  position: fixed;
  z-index: 2;
  transition: all 300ms ease-in-out;
  width: 100%;
  background-color: transparent;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.nav-bar--dark {
  background-color: black;
}

.nav-bar-logo {
  width: 40px;
  height: 27px;
  margin-right: 5px;
}

.nav-bar-title {
  text-decoration: none;
  color: white;
  font-size: 25px;
  display: flex;
  align-items: center;
}

.nav-bar-btn-list {
  display: flex;
}

.nav-bar-btn {
  background-color: transparent;
  color: grey;
  cursor: pointer;
  border: none;
  outline: none;
  padding-left: 40px;
  border: 1px solid transparent;
  padding: 8px 12px;
}

.nav-bar-btn:hover {
  color: white;
}

.nav-left:hover {
  cursor: pointer;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
