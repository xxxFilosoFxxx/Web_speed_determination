<template>
  <div class="q-pa-md">
    <q-form
      @submit="submitFile()"
      class="q-gutter-md">

      <q-file
              label="Предварительный просмотр файла:"
              v-model="file"
              id="video"
              accept="video/*"
              clearable
              filled
              counter
              style="max-width: 400px"
      >
        <template v-slot:prepend>
          <q-icon name="cloud_upload" />
        </template>
      </q-file>

      <q-card>
        <q-card-section>
          <div class="text-h6">Выбор параметров видеозаписи</div>
          <div class="text-subtitle2">выбрать кадр и назначить ширину/высоту</div>
        </q-card-section>

        <q-tabs v-model="tab" class="text-black" indicator-color="orange">
          <q-tab label="Параметры" name="one" />
        </q-tabs>
        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="one">
            <div v-show="file" ref="preview" id="preview"></div>
            <q-separator />

            <div v-show="file">
              <div id="drawingImage">
                <canvas class="canvas" id="canvas1"></canvas>
                <canvas class="canvas" id="canvas2"></canvas>
                <canvas class="canvas" id="canvas3" style="display: none;"></canvas>
                <canvas class="canvas" id="canvas4" style="display: none;"></canvas>

                <input class="input-draw" id="input1" type="text" size="5">
                <input class="input-draw" id="input2" type="text" size="5">
              </div>
              <div class="column items-center">
                <q-btn-group>
                  <q-btn type="submit" push
                         label="Отправить" icon="timeline" color="primary"/>
                  <q-btn id="clearCanvas"  @click="clearCanvas()" push
                         label="Очистить поле" icon="update" color="primary"/>
                  <q-btn id="drawGrid" @click="drawGrid()" push
                         label="Нарисовать сетку" icon="visibility" color="primary"/>
                </q-btn-group>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </q-form>

  </div>
</template>

<script>
  import {useQuasar} from "quasar";
  import { ref } from 'vue';
  import axios from 'axios';
  import { ProjectionCalculator2d } from 'projection-3d-2d';

  export default {
    name: "example",
    data() {
      return {
        file: ref(null),
        videoPreview: ref(null),
        mouse: { x:0, y:0 },
        mouseTo: { x:0, y:0 },
        draw: false,
        countPixel: 0,
        countLine: 0,
        pixels: [],
        pixelsForDraw: [],
        lines: [],
        distance: []
      }
    },
    setup() {
      const $q = useQuasar();
      const tab = ref('one');

      return {
        tab,
        showNotify(filename, id, status) {
          $q.notify({
            color: 'green-4',
            textColor: 'white',
            icon: 'cloud_done',
            message: `Видеозапись ${filename} с id=${id} отправлена на обработку со статусом ${status}`
          });
        }
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
        setAttributes(video, {'width': '1280',
                                     'height': '720',
                                     'controls': '',
                                     'loop': ''});
        video.file = this.file;
        this.videoPreview = video;
        this.$refs.preview.appendChild(video);
        let reader = new FileReader();
        reader.onload = (e) => { this.videoPreview.src = e.target.result; };
        reader.readAsDataURL(this.file);
        // Запуск показа видео и начало обработки пользователем выбранного кадра
        video.addEventListener('play', this.timerCallback, false);
        this.drawPixels();
      }
    },
    methods: {
      distanceEuclid(a, b) {
        return Math.sqrt(Math.pow(b[0] - a[0], 2) + Math.pow(b[1] - a[1], 2));
      },
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
        context.lineWidth = 2;
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
      drawLineUp() {
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
        context.lineWidth = 2;
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
        input1.value = '';
        input2.style.display = 'none';
        input2.value = '';
        this.countLine = 0;
        this.draw = false;
        this.lines = [];
        canvasDraw2.removeEventListener('mousedown', this.drawLineDown, false);
        canvasDraw2.removeEventListener('mousemove', this.drawLineMove, false);
        canvasDraw2.removeEventListener('mouseup', this.drawLineUp, false);

        let canvasGrid = document.getElementById('canvas4');
        let context3 = canvasGrid.getContext("2d");
        context3.clearRect(0, 0, canvasGrid.width, canvasGrid.height);
        this.distance = [];
        canvasGrid.style.display = 'none';
      },
      drawGrid(step = 1) {
        this.distance = [];
        let canvasGrid = document.getElementById('canvas4');
        canvasGrid.style.display = 'block';
        canvasGrid.width = this.videoPreview.width;
        canvasGrid.height = this.videoPreview.height;
        let context = canvasGrid.getContext("2d");
        context.lineWidth = 1;
        context.strokeStyle = 'rgb(0, 255, 0)';
        let width, height;
        width = parseFloat(document.getElementById('input1').value);
        height = parseFloat(document.getElementById('input2').value);
        if (isNaN(width) || isNaN(height)) {
          alert('Введите верные значения расстояния плоксоксти.');
          return false;
        }
        // По расстоянию Евклида соотнесем ширину и высоту для прямоугольника
        let distanceLineWidth = this.distanceEuclid(this.lines[1], this.lines[0]);
        let distanceLineHeight = this.distanceEuclid(this.lines[3], this.lines[2]);
        let distancePixelsWidth = this.distanceEuclid(this.pixels[1], this.pixels[0]);
        let distancePixelsHeight = this.distanceEuclid(this.pixels[2], this.pixels[0]);

        let deltaWidth = distancePixelsWidth / distanceLineWidth;
        let deltaHeight = distancePixelsHeight / distanceLineHeight;
        this.distance.push([0, 0],
                           [width * deltaWidth, 0],
                           [0, height * deltaHeight],
                           [width * deltaWidth, height * deltaHeight]);
        const projectionCalculator = new ProjectionCalculator2d(this.distance, this.pixels);
        let minDistance = projectionCalculator.getUnprojectedPoint([0, 0]);
        let maxDistance = projectionCalculator.getUnprojectedPoint([2048, 1080]);

        context.beginPath();
        for (let x = minDistance[0]; x <= maxDistance[0] + 10; x += step) {
          let pixel2d_1 = projectionCalculator.getProjectedPoint([x, minDistance[1]]);
          let pixel2d_2 = projectionCalculator.getProjectedPoint([x, maxDistance[1]]);
          context.moveTo(pixel2d_1[0], pixel2d_1[1]);
          context.lineTo(pixel2d_2[0], pixel2d_2[1]);
        }
        for (let y = minDistance[1]; y <= maxDistance[1]; y += step) {
          let pixel2d_1 = projectionCalculator.getProjectedPoint([minDistance[0], y]);
          let pixel2d_2 = projectionCalculator.getProjectedPoint([maxDistance[0] + 10, y]);
          context.moveTo(pixel2d_1[0], pixel2d_1[1]);
          context.lineTo(pixel2d_2[0], pixel2d_2[1]);
        }
        context.stroke();
        context.closePath();
      },
      getMatrix() {
        const projectionCalculator = new ProjectionCalculator2d(this.distance, this.pixels);
        return projectionCalculator.resultMatrix;
      },
      submitFile() {
        let formData = new FormData();
        let resultMatrix = this.getMatrix();
        formData.append('file', this.file);
        formData.append('matrix', resultMatrix.toString()); // Матрица 3х3 в виде строки
        axios.post( '/api/load_video',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then((response) => {
          // console.log('SUCCESS!!');
          if (response.status === 202) {
            let task = {filename: response.data['file'], id: response.data['task_id'], status: response.data.status};
            this.showNotify(task.filename, task.id, task.status);
            this.file = ref(null);
          }
        })
        .catch(function(){
          alert('Ошибка обработки видео');
        });
      }
    }
  }
</script>

<style lang="scss">
  #preview {
    /*margin-top: -40px;*/
    position: relative;
    margin: 0 auto 1%;
    width: 1280px;
    height: 720px;
  }
  #drawingImage {
    position: relative;
    margin: 1% auto 0;
    width: 1280px;
    height: 720px;
  }
  .canvas {
    position: absolute;
    left: 0;
    top: 0;
    width:100%;
    height:100%;
  }
  .input-draw {
    display: none;
    outline: none;
    position: absolute;
    background: transparent;
    border-radius: 5px;
    border-color: rgb(255, 0, 0);
    color: rgb(255, 0, 0);
    font-weight: bold;
  }
</style>