<template>
  <q-page padding>
      <q-chat-message v-bind:key="index" v-for="(conversation, index) in conversations"
        :name="conversation.role"
        avatar="https://cdn.quasar.dev/img/avatar4.jpg"
        :text="[conversation.content]"
        sent
        text-html
        size="6"
        stamp="7 minutes ago"
      />
    <!-- content -->
  </q-page>
</template>

<script>


import { ref } from 'vue';
import { useRoute } from 'vue-router'
import { useMainStore } from 'stores/example-store';
import { client } from '../boot/axios'
export default {
  // name: 'PageName',
  methods: {
    async loadStory() {

      let storyTellerOptions = await client.getStoryTellerOptions(this.route.params.id)
      let conversations = await client.getConversation(this.route.params.id)
      this.storyTeller = storyTellerOptions
      this.conversations = conversations.data.conversations
      console.log(this.conversations)
      console.log(conversations)
      console.log(this.conversations)

    },
    async createNewStory() {
      this.storyTeller = this.store.currentStory
      let response = await client.startStoryteller(this.store.currentStory)
      const reader = response.body.getReader()

      reader.read().then(function processText({ done, value }) {
        if (done) {
          return;
        }
        var decoded = new TextDecoder().decode(value);
        const splitted = decoded.split(/\r?\n/);
        for (const stringIndex in splitted) {
          let string = splitted[stringIndex]
          try {
            let parsed = JSON.parse(string)
            if (parsed.type == "stop") {
              let uuidOfConversation = parsed.content
              let conversations = window.localStorage.getItem("conversations")
              if (conversations == null) {
                window.localStorage.setItem("conversations", JSON.stringify([uuidOfConversation]))
              } else {
                let parsedConv = JSON.parse(conversations)
                parsedConv.push(uuidOfConversation)
                window.localStorage.setItem("conversations", JSON.stringify(parsedConv))
              }
            }

          } catch(err) {

          }
        }

        return reader.read().then(processText);
      });

    }
  },
  mounted() {
    if (this.route.params.id == undefined) {
      this.createNewStory()
    } else {
      this.loadStory()
    }
  },
  setup() {
    // const store = useMainStore()
    const route = useRoute()
    const store = useMainStore()
    return {
      route: route,
      conversations: ref([]),
      storyTeller: ref({}),
      store: store
    }
  }
}
</script>
