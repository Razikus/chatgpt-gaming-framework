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
        <q-item clickable :to="'/story/' + item.id" v-bind:key="item.id" v-for="item in conversationsDescription">
          <q-item-section avatar>
            <q-icon name="play_circle" />
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ item.description }}</q-item-label>
            <q-item-label caption>Click to continue the game</q-item-label>
          </q-item-section>
          <q-item-section style="max-width: 30px">
            <q-btn @click="deleteItem(item.id)" dense style="width: 30px">X</q-btn>
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
import { client } from '../boot/axios'

export default defineComponent({
  name: 'MainLayout',

  components: {
  },
  methods: {
    startNewGame() {
      this.$router.push('/newgame')
    },
    deleteItem(what) {
      let conversations = window.localStorage.getItem("conversations")
      if (conversations != null) {
        let parsedConv = JSON.parse(conversations)
        let index = parsedConv.indexOf(what)
        if (index > -1) {
          parsedConv.splice(index, 1);
        }
        window.localStorage.setItem("conversations", JSON.stringify(parsedConv))
        this.fillConversations()
      }
    },
    async fillConversations() {
      this.conversationsDescription = []
      let conversations = window.localStorage.getItem("conversations")
      if (conversations != null) {
        let parsedConv = JSON.parse(conversations)
        for (let index = 0; index < parsedConv.length; index++) {
          const element = parsedConv[index];
          let item = await client.getStoryTellerOptions(element)
          
          this.conversationsDescription.push({
            id: element,
            description: item.data.storyTellerOptions.world.mainGoal
          })

        }
        this.conversations = parsedConv
      }
    }

  },
  mounted() {
    this.fillConversations()
  },
  watch: {
    $route() {
      this.fillConversations()
    }

  },

  setup() {
    const leftDrawerOpen = ref(false)
    const $q = useQuasar()
    $q.dark.set(true)

    return {
      leftDrawerOpen,
      conversations: ref([]),
      conversationsDescription: ref([]),
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
