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
                <canvas id="canvas3" style="display: none;"></canvas>

                <input id="input1" type="text" style="display: none; position: absolute;">
                <input id="input2" type="text" style="display: none; position: absolute;">

              </div>
            </b-col>
          </b-row>
        </b-container>

        <b-button @click="submitFile()">Отправить</b-button>
        <b-button id="clearCanvas" v-show="file" @click="clearCanvas()">Очистить поле</b-button>
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
  import axios from 'axios';
  import ProjectionCalculator2d from 'projection-3d-2d';

  export default {
    name: 'LoadVideo',
    data() {
      return {
        file: null,
        videoPreview: null,
        translationInfo: null,
        mouse: { x:0, y:0 },
        mouseTo: { x:0, y:0 },
        draw: false,
        countPixel: 0,
        countLine: 0,
        pixels: [],
        pixelsForDraw: [],
        lines: [],
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

        this.drawPixels();

        // TODO: обработать матрицу точек и линий
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
      RemoveDrawPixels() {
        let canvasDraw = document.getElementById('canvas2');
        if (this.countPixel >= 4) {
          canvasDraw.removeEventListener('mousedown', this.drawPixel, false);
          this.drawLines();
        }
      },
      RemoveDrawLines() {
        let canvasDraw = document.getElementById('canvas3');
        if (this.countLine >= 2) {
          canvasDraw.removeEventListener('mousedown', this.drawLineDown, false);
          canvasDraw.removeEventListener('mousemove', this.drawLineMove, false);
          canvasDraw.removeEventListener('mouseup', this.drawLineUp, false);
        }
      },
      drawPixel(e) {
        let canvasDraw = document.getElementById('canvas2');
        let context = canvasDraw.getContext("2d");
        this.countPixel += 1;
        // Рисуем опорные точки
        this.mouse.x = e.offsetX;
        this.mouse.y = e.offsetY;
        this.pixels.push([this.mouse.x, this.mouse.y]);

        this.pixelsForDraw.push([this.mouse.x, this.mouse.y, 0]);
        context.beginPath();
        context.arc(this.mouse.x, this.mouse.y, 4, 0, 2 * Math.PI, true)
        context.fill();
        context.closePath();

        if (this.countPixel >= 4) {
          let xMax = canvasDraw.width;
          // Середина многоугольника
          let centerX = 0;
          let centerY = 0;
          for (let i = 0; i < this.pixelsForDraw.length; i++) {
            centerX += this.pixelsForDraw[i][0];
            centerY += this.pixelsForDraw[i][1];
          }
          centerX = centerX / this.pixelsForDraw.length;
          centerY = centerY / this.pixelsForDraw.length;
          // Углы относительно центральной точки многоугольника
          for (let i = 0; i < this.pixelsForDraw.length; i++) {
            let dx = this.pixelsForDraw[i][0] - centerX;
            let dy = this.pixelsForDraw[i][1] - centerY;
            this.pixelsForDraw[i][2] = Math.atan2(dy, dx);
          }
          this.pixelsForDraw.sort(function (a, b) {
            return (a[2] >= b[2]) ? 1 : -1;
          });

          // Соединяем точки
          for (let i = 0; i < this.pixelsForDraw.length - 1; i++) {
            let alfa = (this.pixelsForDraw[i][1] - this.pixelsForDraw[i+1][1]) /
                       (this.pixelsForDraw[i][0] - this.pixelsForDraw[i+1][0]);
            let b = this.pixelsForDraw[i][1] - alfa*this.pixelsForDraw[i][0];
            context.beginPath();
            context.moveTo(0, b);
            context.lineTo(this.pixelsForDraw[i][0], this.pixelsForDraw[i][1] );
            context.lineTo(this.pixelsForDraw[i+1][0], this.pixelsForDraw[i+1][1] );
            context.lineTo(xMax, alfa*xMax+b);
            context.stroke();
            context.closePath();
          }
          let alfa = (this.pixelsForDraw[3][1] - this.pixelsForDraw[0][1]) /
                     (this.pixelsForDraw[3][0] - this.pixelsForDraw[0][0]);
          let b = this.pixelsForDraw[3][1] - alfa*this.pixelsForDraw[3][0];
          context.beginPath();
          context.moveTo(0, b);
          context.lineTo(this.pixelsForDraw[3][0], this.pixelsForDraw[3][1] );
          context.lineTo(this.pixelsForDraw[0][0], this.pixelsForDraw[0][1] );
          context.lineTo(xMax, alfa*xMax+b);
          context.stroke();
          context.closePath();
          this.RemoveDrawPixels();
        }
      },
      drawPixels() {
        let canvasDraw = document.getElementById('canvas2');
        let context = canvasDraw.getContext("2d");
        canvasDraw.width = this.videoPreview.width;
        canvasDraw.height = this.videoPreview.height;
        context.lineWidth = 3;
        context.strokeStyle = 'rgb(0, 255, 0)';
        context.fillStyle = 'rgb(0, 255, 0)';

        canvasDraw.addEventListener('mousedown', this.drawPixel, false);
      },
      drawLineDown(e) {
        let canvasDraw = document.getElementById('canvas3');
        let context = canvasDraw.getContext("2d");
        this.countLine += 1;
        this.mouse.x = e.offsetX;
        this.mouse.y = e.offsetY;
        this.lines.push([this.mouse.x, this.mouse.y]);
        context.beginPath();
        context.arc(this.mouse.x, this.mouse.y, 4, 0, 2 * Math.PI, true)
        context.fill();
        context.moveTo(this.mouse.x, this.mouse.y);
        this.draw = true;
      },
      drawLineMove(e) {
        if (this.draw) {
          this.mouseTo.x = e.offsetX;
          this.mouseTo.y = e.offsetY;
        }
      },
      drawLineUp: function (e) {
        if (this.draw) {
          let canvasDraw = document.getElementById('canvas3');
          let input1 = document.getElementById('input1');
          let input2 = document.getElementById('input2');
          let context = canvasDraw.getContext("2d");
          this.lines.push([this.mouseTo.x, this.mouseTo.y]);
          context.arc(this.mouseTo.x, this.mouseTo.y, 4, 0, 2 * Math.PI, true)
          context.fill();
          context.lineTo(this.mouseTo.x, this.mouseTo.y);
          context.stroke();
          context.closePath();
          this.draw = false;
          if (this.countLine === 1) {
            let alfa = (this.mouseTo.y - this.mouse.y) / (this.mouseTo.x - this.mouse.x);
            let deltaX = (this.mouseTo.x + this.mouse.x) / 2;
            let deltaY = (this.mouseTo.y + this.mouse.y) / 2;
            if (Math.atan(alfa) < 0) {
              deltaY += 15;
              input1.style.left = deltaX + 'px';
              input1.style.top = deltaY + 'px';
              input1.style.display = 'block';
            } else {
              deltaY -= 40;
              input1.style.left = deltaX + 'px';
              input1.style.top = deltaY + 'px';
              input1.style.display = 'block';
            }
          }
          if (this.countLine >= 2) {
            let alfa = (this.mouseTo.y - this.mouse.y) / (this.mouseTo.x - this.mouse.x);
            let deltaX = (this.mouseTo.x + this.mouse.x) / 2;
            let deltaY = (this.mouseTo.y + this.mouse.y) / 2;
            if (Math.atan(alfa) < 0) {
              deltaY += 15;
              input2.style.left = deltaX + 'px';
              input2.style.top = deltaY + 'px';
              input2.style.display = 'block';
            } else {
              deltaY -= 40;
              input2.style.left = deltaX + 'px';
              input2.style.top = deltaY + 'px';
              input2.style.display = 'block';
            }
            this.RemoveDrawLines();
          }
        }
      },
      drawLines() {
        let canvasDraw = document.getElementById('canvas3');
        let context = canvasDraw.getContext("2d");
        canvasDraw.width = this.videoPreview.width;
        canvasDraw.height = this.videoPreview.height;
        context.lineWidth = 3;
        context.strokeStyle = 'rgb(255, 0, 0)';
        context.fillStyle = 'rgb(255, 0, 0)';

        canvasDraw.style.display = 'block';
        canvasDraw.addEventListener('mousedown', this.drawLineDown, false);
        canvasDraw.addEventListener('mousemove', this.drawLineMove, false);
        canvasDraw.addEventListener('mouseup', this.drawLineUp, false);
      },
      clearCanvas() {
        let canvasDraw1 = document.getElementById('canvas2');
        let context1 = canvasDraw1.getContext("2d");
        context1.clearRect(0, 0, canvasDraw1.width, canvasDraw1.height);
        this.countPixel = 0;
        this.pixels = [];
        this.pixelsForDraw = [];
        canvasDraw1.removeEventListener('mousedown', this.drawPixel, false);
        canvasDraw1.addEventListener('mousedown', this.drawPixel, false);

        let canvasDraw2 = document.getElementById('canvas3');
        let input1 = document.getElementById('input1');
        let input2 = document.getElementById('input2');
        let context2 = canvasDraw2.getContext("2d");
        context2.clearRect(0, 0, canvasDraw2.width, canvasDraw2.height);
        canvasDraw2.style.display = 'none';
        input1.style.display = 'none';
        input2.style.display = 'none';
        this.countLine = 0;
        this.draw = false;
        this.lines = [];
        canvasDraw2.removeEventListener('mousedown', this.drawLineDown, false);
        canvasDraw2.removeEventListener('mousemove', this.drawLineMove, false);
        canvasDraw2.removeEventListener('mouseup', this.drawLineUp, false);
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
  #canvas3 {
    position: absolute;
    left: 0;
    top: 0;
    width:100%;
    height:100%;
  }
</style>
