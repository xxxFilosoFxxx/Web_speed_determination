<template>
  <div>
    <b-container>
<!--      <input type="file" id="video" ref="file" accept="video/*" @change="handleFileUpload()">-->
<!--      <video width="500" height="300" muted controls loop :src="videoPreview" v-show="showPreview"></video>-->
<!--      <b-button @click="submitFile()">Submit</b-button>-->

      <b-form-group label="Предварительный просмотр файла:" label-for="video">
        <b-form-file
          id="video"
          v-model="file"
          accept="video/*" plain
        ></b-form-file>
        <div v-if="file">
          <p>Название файла: {{file.name}}</p>
          <p>Размер: {{file.size}} </p>
          <p>Тип: {{file.type}}</p>
        </div>
        <div ref="preview" id="preview"></div>
        <b-button @click="submitFile()">Отправить</b-button>
      </b-form-group>
    </b-container>

    <b-container>
      <h3 class="mt-5">Прямая трансляция</h3>
      <b-img :src="imgURL" thumbnail fluid-grow alt=""></b-img>
    </b-container>

  </div>
</template>

<script>
  /* eslint-disable */
  import axios from 'axios'

  export default {
    name: 'LoadVideo',
    data() {
      return {
        file: null,
        videoPreview: null,
        image: '',
        imgURL: 'http://localhost:8000/main/load_video/'
      }
    },
    watch: {
      file(val) {
        function setAttributes(el, options) {
           Object.keys(options).forEach(function(attr) {
             el.setAttribute(attr, options[attr]);
           })
        }
        if (!val) return;
        if (this.videoPreview) {
          this.videoPreview.remove();
        }

        let video = document.createElement("video");
        setAttributes(video, {'width': '640', 'height': '480', 'controls': '', 'loop': ''});
        video.file = this.file;
        this.videoPreview = video;
        this.$refs.preview.appendChild(video);

        let reader = new FileReader();
        reader.onload = (e) => { this.videoPreview.src = e.target.result; };
        reader.readAsDataURL(this.file);
      }
    },
    methods: {
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
