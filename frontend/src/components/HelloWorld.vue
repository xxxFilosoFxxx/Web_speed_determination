<template>
<!--  <h3>{{message}}</h3>-->

<!--  <label>File-->
<!--    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>-->
<!--  </label>-->

<!--  <div>-->
<!--    <video width="500" height="300" controls loop>-->
<!--      <source src="static/data_video/видеонаблюдение.mp4" type='video/mp4'>-->
<!--      &lt;!&ndash;    <source src="static/data_video/video.webm" type='video/webm'>&ndash;&gt;-->
<!--      Видео не работает!-->
<!--    </video>-->
<!--  </div>-->

  <div>
    <form action="/" method="post">
      <label for="video">Select image:</label>
      <input type="file" id="video" name="video" accept="video/*">
      <input type="submit">
    </form>
  </div>


</template>

<script>
/* eslint-disable */
  export default {
    name: 'HelloWorld',
    data() {
      return {
        message: ''
      }
    },
    methods: {
      async fetchMessage() {
        // TODO:
        const response = await fetch('http://localhost:8000/main/')
        this.message = await response.json()
        this.message = this.message['message']
      }
    },
    async created() {
      await this.fetchMessage()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
