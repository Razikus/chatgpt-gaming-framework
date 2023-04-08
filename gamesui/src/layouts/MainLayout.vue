<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="banner">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          GPT Games v0.1.0
        </q-toolbar-title>

      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>

        <q-item-label header>
          New game
        </q-item-label>
        <q-item clickable @click="startNewGame">
          <q-item-section avatar>
            <q-icon name="play_arrow" />
          </q-item-section>

          <q-item-section>
            <q-item-label>Start a new game</q-item-label>
            <q-item-label caption>Click to start a new story</q-item-label>
          </q-item-section>
        </q-item>
        <q-item-label header>
          Your games
        </q-item-label>
        <q-item clickable :to="'/story/' + item" v-bind:key="item" v-for="item in conversations">
          <q-item-section avatar>
            <q-icon name="play_circle" />
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ item }}</q-item-label>
            <q-item-label caption>Click to continue the game</q-item-label>
          </q-item-section>
        </q-item>

      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style>
.banner {
  background-color: #4f0e0e;
}
</style>

<script>
import { defineComponent, ref } from 'vue'

import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'MainLayout',

  components: {
  },
  methods: {
    startNewGame() {
      this.$router.push('/newgame')
    }

  },
  mounted() {
    let conversations = window.localStorage.getItem("conversations")
    if (conversations != null) {
      let parsedConv = JSON.parse(conversations)
      this.conversations = parsedConv

    }


  },

  setup() {
    const leftDrawerOpen = ref(false)
    const $q = useQuasar()
    $q.dark.set(true)

    return {
      leftDrawerOpen,
      conversations: ref([]),
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
