<template>
  <div class="q-pa-md" style="max-width: 400px">
    <q-form
        @submit="submitRegister"
        @reset="onReset"
        class="q-gutter-md">

      <q-input outlined
               v-model="login"
               label="Логин"
               lazy-rules
               :rules="[
                  val => val && val.length > 0 || 'Введите логин'
                ]"/>

      <q-input outlined
               :type="isPwd ? 'password' : 'text'"
               v-model="password"
               label="Пароль"
               lazy-rules
               :rules="[
                  val => val && val.length > 0 || 'Введите пароль'
               ]">
        <template v-slot:append>
          <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
          />
        </template>
      </q-input>
      <div>
        <q-btn type="submit" label="Зарегестрироваться" color="indigo-10" />
        <q-btn type="reset" label="Сбросить" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>

  </div>
</template>

<script>
import {useQuasar} from "quasar";
import { ref } from "vue";

export default {
  name: "RegisterForm",

  setup() {
    const $q = useQuasar();

    const login = ref(null);
    const password = ref(null);

    return {
      login,
      password,
      isPwd: ref(true),

      submitRegister () {
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'cloud_done',
          message: 'Задача отправлена на обработку'
        })
      },

      onReset () {
        login.value = null;
        password.value = null;
      }
    }
  }
}
</script>

<style scoped>

</style>