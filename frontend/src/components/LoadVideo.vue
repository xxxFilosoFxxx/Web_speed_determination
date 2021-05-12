<template>
  <div class="container">
    <label for="video">File Preview:</label>
    <input type="file" id="video" ref="file" accept="video/*" v-on:change="handleFileUpload()">
    <video width="500" height="300" muted controls loop v-bind:src="videoPreview" v-show="showPreview"></video>
    <button v-on:click="submitFile()">Submit</button>
  </div>

<!--  <div>-->
<!--    <img src="http://localhost:8000/main/load_video/" width="100%">-->
<!--  </div>-->

</template>

<script>
  /* eslint-disable */
  import axios from 'axios'

  export default {
    name: 'HelloWorld',
    data() {
      return {
        file: '',
        showPreview: false,
        videoPreview: ''
      }
    },
    methods: {
      // async fetchMessage() {
      //   // TODO:
      //   const response = await fetch('http://localhost:8000/main/')
      //   this.message = await response.json()
      //   this.message = this.message['message']
      // },
      handleFileUpload() {
        this.file = this.$refs.file.files[0];
        let reader  = new FileReader();

        reader.addEventListener("load", function () {
          this.showPreview = true;
          this.videoPreview = reader.result;
        }.bind(this), false);
        if( this.file ) {
          reader.readAsDataURL( this.file );
        }
      },
      submitFile() {
        let formData = new FormData();
        formData.append('file', this.file);
        axios.post( 'http://localhost:8000/main/load_video/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },
    },
    // async created() {
    //   await this.fetchMessage()
    // }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
