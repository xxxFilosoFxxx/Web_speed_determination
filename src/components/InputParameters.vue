<template>
  <div class="q-pa-md" style="max-width: 400px">
    <q-form
        @submit="submitTask"
        @reset="onReset"
        class="q-gutter-md">

      <q-input outlined
               type="number"
               v-model="msisdn"
               label="Число"
               lazy-rules
               :rules="[
                  val => val !== null && val !== '' || 'Введите число'
                ]"/>
      <q-input outlined
               type="number"
               v-model="radius"
               label="Радиус"
               lazy-rules
               :rules="[
                  val => val !== null && val !== '' || 'Введите радиус'
               ]"/>
      <q-input outlined
               type="number"
               v-model="delta"
               label="Дельта"
               lazy-rules
               :rules="[
                  val => val !== null && val !== '' || 'Введите дельту'
               ]"/>
      <div>
        <q-btn outline type="submit" label="Отправить" style="color: goldenrod;" />
        <q-btn type="reset" label="Сбросить" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>

  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from "vue";

export default {
  name: "InputParameters",

  setup() {
    const $q = useQuasar();

    const msisdn = ref(null);
    const radius = ref(null);
    const delta = ref(null);

    return {
      msisdn,
      radius,
      delta,

      submitTask () {
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'cloud_done',
          message: 'Задача отправлена на обработку'
        })
      },

      onReset () {
        msisdn.value = null;
        radius.value = null;
        delta.value = null;
      }
    }
  }
}

</script>

<style scoped>

</style>