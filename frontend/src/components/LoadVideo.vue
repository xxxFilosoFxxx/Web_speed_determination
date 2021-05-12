<template>
<!--  eslint-disable -->
  <div class="container">

    <div>
      <label for="video">File Preview:</label>
      <input type="file" id="video" ref="file" accept="video/*" v-on:change="handleFileUpload()">
      <video width="500" height="300" muted controls loop v-bind:src="videoPreview" v-show="showPreview"></video>
      <button v-on:click="submitFile()">Submit</button>
    </div>

    <div class="container">
      <h3 class="mt-5">Live Streaming</h3>
      <img v-bind:src="imgURL" width="100%">
    </div>
  </div>
</template>

<script>
  /* eslint-disable */
  import axios from 'axios'

  export default {
    name: 'LoadVideo',
    data() {
      return {
        file: '',
        showPreview: false,
        videoPreview: '',
        image: '',
        imgURL: 'http://localhost:8000/main/load_video/'
      }
    },
    methods: {
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
      // async fetchMessage() {
      //   const response = await fetch('http://localhost:8000/main/load_video/')
      //   this.message = await response.json()
      //   this.message = this.message['message']
      // },
    },
    // async created() {
    //   await this.fetchMessage()
    // }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
