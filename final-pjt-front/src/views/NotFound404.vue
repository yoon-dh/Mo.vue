<template>
  <div>
    <img
      class="black-image_under"
      src="@/assets/HomeView/Home/blackimage.png"
      alt=""
    />
    <img
      class="background-img"
      src="@/assets/HomeView/Home/404joker.jpg"
      data-aos="fade-zoom-in"
      data-aos-easing="ease-in-back"
      data-aos-delay="1000"
      data-aos-offset="0"
      data-aos-duration="2000"
    />
    <p
      class="not-found"
      data-aos="fade-zoom-in"
      data-aos-easing="ease-in-back"
      data-aos-delay="100"
      data-aos-offset="0"
      data-aos-duration="2000"
    >
      404 Not Found
    </p>
  </div>
</template>

<script>
export default {
  name: "NotFound404",
};
</script>

<style>
.not-found {
  position: absolute;
  top: 10%;
  left: 38%;
  color: white;
  font-size: 50px;
  font-weight: bold;
}
</style>
