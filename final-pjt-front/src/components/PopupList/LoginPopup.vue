<template>
  <!-- <div class="login-pop-up">
    <div class="login-popup-top">
      <div>LOGIN</div>
      <img
        @click="closePopup"
        class="popup-close"
        src="@/assets/HomeView/Home/close.png"
        alt=""
      />
    </div>
    <div class="login-popup-bottom">
      <div class="login-popup-main">
        <label for="username">ID : </label>
        <input id="username" type="text" v-model="username" />
        <br />
        <label for="password">PASSWORD : </label>
        <input id="password" type="password" v-model="password" />
        <br />
      </div>
      <button @click="toSignup">Sign-up</button>
      <button @click="login">Login</button>
    </div>
  </div> -->
  <div class="login-pop-up">
    <div class="login-popup-top">
      <div><b>Login</b></div>
      <img
        @click="closePopup"
        class="popup-close"
        src="@/assets/HomeView/Home/close-white.png"
        alt=""
      />
    </div>
    <div class="login-popup-bottom">
      <div class="login-popup-main">
        <input
          id="username"
          placeholder="User name"
          type="text"
          v-model="username"
          el
        />

        <br />

        <input
          id="password"
          placeholder="Password"
          type="password"
          v-model="password"
        />

        <br />
      </div>
      <div class="login-button-group">
        <button class="login-button" @click="login">Login</button>
        <hr />
        <p>아직 회원이 아니신가요?</p>

        <button class="login-button" @click="toSignup">Sign-up</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPopup",

  data() {
    return {
      username: null,
      password: null,
    };
  },

  methods: {
    closePopup() {
      this.$store.commit("LOGIN_POPUP_CLOSE");
    },

    login() {
      const username = this.username;
      const password = this.password;

      const payload = {
        username,
        password,
      };

      this.$store.dispatch("login", payload);
    },

    toSignup() {
      this.$store.commit("LOGIN_POPUP_CLOSE");
      this.$store.commit("SIGNUP_POPUP_OPEN");
    },
  },
};
</script>

<style>
.login-pop-up {
  padding: 30px;
  border-radius: 8px;
  color: #fff;
}

.login-popup-top {
  padding-bottom: 20px;
}

.login-popup-main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0px 50px;
}

.login-button {
  width: 60%;
  height: 40px;
  margin: auto;
  justify-content: center;
  display: block;
  color: #fff;
  background: #080808c3;
  border: 1px solid white;
  font-size: 1em;
  font-weight: bold;
  /* margin-top: 10px; */
  outline: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}
.login-button:hover {
  background: #ffffffea;
  color: rgb(0, 0, 0);
}

/* .login-button-group {
  display: flex;
} */
</style>
