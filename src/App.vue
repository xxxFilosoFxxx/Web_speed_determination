<template>
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5dc33da (v2.0.1)
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="glossy">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Essential Links</q-item-label>
        <q-item clickable tag="a" target="_blank" href="https://quasar.dev">
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Docs</q-item-label>
            <q-item-label caption>quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://github.com/quasarframework/">
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Github</q-item-label>
            <q-item-label caption>github.com/quasarframework</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://chat.quasar.dev">
          <q-item-section avatar>
            <q-icon name="chat" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Discord Chat Channel</q-item-label>
            <q-item-label caption>chat.quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://forum.quasar.dev">
          <q-item-section avatar>
            <q-icon name="forum" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Forum</q-item-label>
            <q-item-label caption>forum.quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://twitter.com/quasarframework">
          <q-item-section avatar>
            <q-icon name="rss_feed" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Twitter</q-item-label>
            <q-item-label caption>@quasarframework</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <HelloWorld />
    </q-page-container>
<<<<<<< HEAD
=======
=======
  <q-layout view="lHh lpR lFf">

    <q-header elevated class="bg-indigo-10 text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-btn round to="/">
            <q-avatar size="40px">
              <img class="logo-img" src="@/assets/clipboard.png"/>
            </q-avatar>
          </q-btn>
           Приложение для отправки задач в очередь
        </q-toolbar-title>
      </q-toolbar>

<!--      <q-tabs v-model="tab">-->
      <q-tabs class="text-teal" narrow-indicator>
        <q-tab name="username" icon="assignment_ind" label="$store.state.username" />
        <q-tab name="logout" label="Выйти" to="/logout"/>
      </q-tabs>
    </q-header>

    <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        :width="300"
        :breakpoint="700"
        bordered
        class="bg-indigo-10 text-white">
<!--      // TODO: прописать ссылки к выпадающим задачам-->
      <q-scroll-area class="fit">
        <q-list padding class="menu-list" >
          <q-item clickable v-ripple to="/" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="inbox" />
            </q-item-section>

            <q-item-section>
              Главная страница
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/about" active-class="text-orange">
            <q-item-section avatar>
              <q-icon name="star" />
            </q-item-section>

            <q-item-section>
              Список задач
            </q-item-section>
          </q-item>

          <q-separator dark/>

          <q-item clickable v-ripple v-for="n in 5" :key="n">
            <q-item-section>`Здесь появляется задача`</q-item-section>
            <q-item-section avatar>
              <q-avatar color="positive"></q-avatar>
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
  </q-layout>
</template>

<script>
import { ref } from 'vue'
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 5dc33da (v2.0.1)
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'LayoutDefault',

  components: {
    HelloWorld
  },

  setup () {
    return {
      leftDrawerOpen: ref(false)
    }
  }
}
</script>
<<<<<<< HEAD
=======
=======

export default {
  name: 'BasePage',

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
}
</script>
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
