<template>
  <div class="signup-pop-up">
    <div class="signup-popup-top">
      <div><b>Sign Up</b></div>
      <img
        class="popup-close"
        src="@/assets/HomeView/Home/close-white.png"
        alt=""
        @click="closePopup"
      />
    </div>
    <div class="signup-popup-bottom">
      <div class="signup-popup-main">
        <input
          id="username"
          placeholder="User name"
          type="text"
          v-model="username"
        />
        <br />
        <input
          id="password1"
          placeholder="Password"
          type="password"
          v-model="password1"
        />
        <br />
        <input
          id="password2"
          placeholder="Confirm Password"
          type="password"
          v-model="password2"
        />
        <br />
      </div>
      <button class="signup-button" @click="signUp">Sign-up</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupPopup",

  data() {
    return {
      username: null,
      password1: null,
      password2: null,
    };
  },

  methods: {
    closePopup() {
      this.$store.commit("SIGNUP_POPUP_CLOSE");
    },

    signUp() {
      const username = this.username;
      const password1 = this.password1;
      const password2 = this.password2;

      const payload = {
        username,
        password1,
        password2,
      };

      this.$store.dispatch("signUp", payload);
    },
  },
};
</script>

<style>
.signup-pop-up {
  padding: 30px;
  border-radius: 8px;
  color: #fff;
}

.signup-popup-top {
  padding-bottom: 20px;
}

.signup-popup-main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0px 50px;
}
.signup-button {
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
  outline: none;
  border-radius: 5px;
  transition: 0.2s ease-in;
  cursor: pointer;
}

.signup-button:hover {
  background: #ffffffea;
  color: rgb(0, 0, 0);
}
</style>
