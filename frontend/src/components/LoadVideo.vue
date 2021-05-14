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
        <b-button @click="submitFile()">Отправить</b-button>
      </b-form-group>
    </b-container>

    <b-container ref="translation" id="translation">
      <h3 class="mt-5">Прямая трансляция</h3>
      <b-img id="image" thumbnail fluid-grow alt=""></b-img>
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
        // image: null,
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

        let translation = this.imgURL + this.file.name;
        axios.get(translation)
        .then(function(){
          console.log('translations SUCCESS!!');
        })
        .catch(function(){
          console.log('translation FAILURE!!');
        });

        let img = document.getElementById('image');
        img.src = translation;
      },
      // async fetchImages() {
      //   const response = await fetch('http://localhost:8000/main/load_video');
      //   const data = await response.blob();
      //   this.image = URL.createObjectURL(data);
      //
      //   let img = document.createElement('img');
      //   img.src = this.image;
      //   this.$refs.translation.appendChild(img);
      // },
    },
    // async created() {
    //   await this.fetchImages();
    // }
  }
</script>

<style>
  #preview {
    /*margin-top: -40px;*/
  }
</style>
