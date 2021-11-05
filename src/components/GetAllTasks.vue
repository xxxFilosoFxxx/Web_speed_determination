<template>
  <div class="q-pa-md">
    <q-table
      title="Все видео"
      :rows="rows"
      :columns="columns"
      row-key="task_id"
      :separator="'cell'"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="task_id" :props="props">
            {{ props.row['task_id'] }}
          </q-td>
          <q-td key="filename" :props="props">
            <q-badge color="green">
              {{ props.row.filename }}
            </q-badge>
          </q-td>
          <q-td key="video" :props="props">
            <div v-if="props.row.video !== null && props.row.video !== undefined">
              <div>
                <video :src="sourceVideo(props.row.video)" width="400" height="300" controls></video>
              </div>
              <q-btn color="negative" label="Удалить" @click="deleteVideo(props.row.filename, props.row['task_id'])"/>
            </div>
          </q-td>
          <q-td key="status" :props="props">
            {{ props.row.status }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import {useQuasar} from "quasar";
import axios from "axios";

export default {
  name: "GetAllTasks",
    data() {
      return {
        columns: [{
          name: 'task_id',
          required: true,
          label: 'Id Видео',
          align: 'left',
          field: row => row['task_id'],
          format: val => `${val}`
          },
          { name: 'filename', align: 'center', label: 'Название', field: 'filename'},
          { name: 'video', align: 'center', label: 'Видеофайл', field: 'video'},
          { name: 'status', align: 'right', label: 'Статус', field: 'status'}
        ],
        rows: this.$store.state.allTasksList
      }
    },
    setup() {
      const $q = useQuasar();

      return {
        showNotify(filename, task_id) {
          $q.notify({
            color: 'red-4',
            textColor: 'white',
            icon: 'cloud_done',
            message: `Видеозапись ${filename} с id=${task_id} была успешно удалена`
          });
        }
      }
    },
    methods: {
      sourceVideo(videoName) {
        return '/source_video/' + videoName;
      },
      deleteVideo(fileName, taskId) {
        axios.get('/delete_task', { params: { task_id: taskId, filename: fileName } })
          .then((response) => {
              this.showNotify(response.data.filename, response.data.task_id);
          })
          .catch(function () {
              alert('Ошибка при удалении видеофайла');
          });
      }
    }
  }
</script>
<style scoped>

</style>