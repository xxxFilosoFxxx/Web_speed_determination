<template>
  <div class="home">
    <load-video/>
  </div>
</template>

<script>

import LoadVideo from "@/components/LoadVideo";

export default {
  name: 'Home',
  components: {
    LoadVideo
  }
}
</script>

<style lang="scss">
  @import "src/styles/quasar";
  @import "src/styles/quasar.variables.sass";

  body {
    background-color: $grey-2;
  }

  .logo-img {
    cursor: pointer;
    transition: 0.5s linear;
  }
  .logo-img:hover {
    -webkit-transform: scale(0.9);
    transform: scale(0.9);
  }
</style>
