<template>
  <div class="container-fluid p-3 bg-light">
    <b-container fluid="lg">

      <b-form-group label="Предварительный просмотр файла:" label-class="h3" label-for="video">
        <b-form-file id="video"  v-model="file" accept="video/*" plain></b-form-file>

        <b-container class="p-3" v-if="file">
          <b-row>
            <b-col> Название файла: {{file.name}} </b-col>
            <b-col> Размер: {{file.size}} байт </b-col>
            <b-col> Тип: {{file.type}} </b-col>
          </b-row>
        </b-container>

        <b-container>
          <b-row>
            <b-col ref="preview" id="preview"></b-col>
            <div class="w-100"></div>
            <b-col v-show="file">
              <p class="h3">Область для выбора параметров видеозаписи:</p>
              <div id="drawingImage">
                <canvas id="canvas1"></canvas>
                <canvas id="canvas2"></canvas>
              </div>
            </b-col>
          </b-row>
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
        mouse: { x:0, y:0 },
        imgURL: 'http://localhost:8000/main/live_video/'
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

        let video = document.createElement('video');
        setAttributes(video, {'width': '1280', 'height': '720', 'controls': '', 'loop': ''});
        video.file = this.file;
        this.videoPreview = video;
        this.$refs.preview.appendChild(video);
        let reader = new FileReader();
        reader.onload = (e) => { this.videoPreview.src = e.target.result; };
        reader.readAsDataURL(this.file);

        video.addEventListener('play', this.timerCallback, false);

        this.drawOnCanvas();
      }
    },
    methods: {
      computeFrame() {
        let canvas = document.getElementById('canvas1');
        canvas.width = this.videoPreview.width;
        canvas.height = this.videoPreview.height;

        let ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoPreview, 0, 0, this.videoPreview.width, this.videoPreview.height);
        // const frame = ctx.getImageData(0, 0, this.vueVideo.width, this.vueVideo.height);
      },
      timerCallback() {
        if (this.videoPreview.paused || this.videoPreview.ended) { return; }
          this.computeFrame();
          setTimeout(this.timerCallback,0);
      },
      drawOnCanvas() {
        let mouse = { x:0, y:0};
        this.mouse = mouse;
        let draw = false;
        let canvasDraw = document.getElementById('canvas2');
        let context = canvasDraw.getContext("2d");
        canvasDraw.width = this.videoPreview.width;
        canvasDraw.height = this.videoPreview.height;

        canvasDraw.addEventListener('mousedown', (e) => {
            mouse.x = e.offsetX;
            mouse.y = e.offsetY;
            draw = true;
            context.strokeStyle = 'rgb(0, 255, 0)';
            context.beginPath();
            context.moveTo(mouse.x, mouse.y);
          }, false);

        canvasDraw.addEventListener('mousemove', (e) => {
          if (draw) {
            mouse.x = e.offsetX;
            mouse.y = e.offsetY;
            context.lineTo(mouse.x, mouse.y);
            context.stroke();
          }
        }, false);

        canvasDraw.addEventListener('mouseup', (e) => {
          mouse.x = e.offsetX;
          mouse.y = e.offsetY;
          context.lineTo(mouse.x, mouse.y);
          context.stroke();
          context.closePath();
          draw = false;
        }, false);
      },
      getTranslation() {
        this.translationInfo = this.imgURL + this.file.name;
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
  #drawingImage {
    position: relative;
    width: 1280px;
    height: 720px;
  }
  #canvas1 {
    position: absolute;
    left: 0;
    top: 0;
    width:100%;
    height:100%;
  }
  #canvas2 {
    position: absolute;
    left: 0;
    top: 0;
    width:100%;
    height:100%;
  }
</style>
