<template>
  <div class="p-3 bg-light">
    <b-container>

      <b-form-group label="Предварительный просмотр файла:" label-class="h3" label-for="video">
        <b-form-file id="video"  v-model="file" accept="video/*" plain></b-form-file>

        <b-container class="p-3" v-if="file">
          <b-row>
            <b-col> Название файла: {{file.name}} </b-col>
            <b-col> Размер: {{file.size}} </b-col>
            <b-col> Тип: {{file.type}} </b-col>
          </b-row>
        </b-container>

        <div ref="preview" id="preview"></div>

        <b-container v-show="file">
          <canvas id="canvas" width="640" height="480"></canvas>
        </b-container>

        <b-button @click="submitFile()">Отправить</b-button>
      </b-form-group>
    </b-container>

    <b-container v-if="translationInfo">
      <h3 class="mt-5">Прямая трансляция</h3>
      <b-img ref="translation" id="translation" :src="translationInfo" thumbnail fluid-grow alt=""></b-img>
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
        translationInfo: null,
        imgURL: 'http://localhost:8000/main/live_video/'
      }
    },
    // mounted() {
    //   let canvas = document.getElementById('canvas');
    //   this.vueCanvas = canvas.getContext('2d');
    // },
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

        let video = document.createElement('video');
        setAttributes(video, {'width': '640', 'height': '480', 'controls': '', 'loop': ''});
        video.file = this.file;
        this.videoPreview = video;
        this.$refs.preview.appendChild(video);

        let reader = new FileReader();
        reader.onload = (e) => { this.videoPreview.src = e.target.result; };
        reader.readAsDataURL(this.file);

        let canvas = document.getElementById('canvas');
        let ctx = canvas.getContext('2d');
        video.addEventListener('play', function() {
          ctx.drawImage(video, 0, 0, video.width, video.height);
          let frame = ctx.getImageData(0, 0, video.width, video.height);
        });
      }
    },
    methods: {
      // updateCanvas() {
      //   this.canvas = document.getElementById('canvas');
      //   this.ctx = this.canvas.getContext('2d');
      //
      // },
      getTranslation() {
        this.translationInfo = this.imgURL + this.file.name;
        // let video = document.getElementById('video');
        // video.addEventListener('play', function() {
        //   this.vueCanvas.drawImage(video, 0, 0, '640', '480');
        //   let frame = this.vueCanvas.getImageData(0, 0, '640', '480');
        // });
        axios.get(this.translationInfo)
        .then((response) => {
          console.log('translations SUCCESS!!');
          if (response.status === 200) {
            this.translationInfo = null;
          }
        })
        .catch(function(){
          console.log('translation FAILURE!!');
        });
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
        ).then((response) => {
          console.log('SUCCESS!!');
          if (response.status === 200) {
            this.getTranslation();
          }
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      }
    },
  }
</script>

<style>
  #preview {
    /*margin-top: -40px;*/
  }
</style>
