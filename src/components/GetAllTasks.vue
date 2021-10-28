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
            <video v-if="props.row.video !== null && props.row.video !== undefined" :src="sourceVideo(props.row.video)"
                   width="400" height="300" controls>
<!--              <source :src="sourceVideo(props.row.video)" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'>-->
            </video>
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
  methods: {
    sourceVideo(videoName) {
      return '/source_video/' + videoName;
    }
  }
}
</script>
<style scoped>

</style>