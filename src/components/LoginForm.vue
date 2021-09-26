<template>
  <div class="q-pa-md" style="max-width: 400px">
    <q-form
        @submit.prevent="submitLogin"
        @reset="onReset"
        class="q-gutter-md">
      <!--Везде писать как выше .prevent-->
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

      <q-toggle v-model="accept" label="Запомнить меня" />

      <div>
        <q-btn type="submit" label="Отправить" color="indigo-10" />
        <q-btn type="reset" label="Сбросить" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>

  </div>
</template>

<script>
import {useQuasar} from "quasar";
import { ref } from "vue";

export default {
  name: "LoginForm",

  setup() {
    const $q = useQuasar();

    const login = ref(null);
    const password = ref(null);
    const accept = ref(false);

    return {
      login,
      password,
      accept,
      isPwd: ref(true),

      submitLogin () {
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
        accept.value = false;
      }
    }
  }
}
</script>

<style scoped>

</style>