<template>
  <q-page padding>
    <q-chat-message v-bind:key="index" v-for="(conversation, index) in filteredConversations" :name="conversation.role"
      avatar="https://cdn.quasar.dev/img/avatar4.jpg" :text="[conversation.content]" :sent="conversation.role != 'assistant'" size="6" stamp="7 minutes ago">
      <template v-slot:default>
        <p class="conversation">{{ conversation.content }}</p>
      </template>
    </q-chat-message>
    <q-chat-message name="You" avatar="https://cdn.quasar.dev/img/avatar4.jpg" size="6" sent v-if="!assistantWriting">
      <template v-slot:default>
        <div>
          Choose:
          <q-btn color="black" @click="continueWith(1)">1)</q-btn>
          <q-btn color="black" @click="continueWith(2)" style="margin-left: 5px">2)</q-btn>
          <q-btn color="black" @click="continueWith(3)" style="margin-left: 5px">3)</q-btn>
          <div style="margin-top: 10px">
            Or write your own answer:
            <q-input v-model="ownNewMessage"></q-input>

          </div>
        </div>
      </template>
    </q-chat-message>
    <q-chat-message name="assistant" avatar="https://cdn.quasar.dev/img/avatar4.jpg" size="6" sent v-else>
      <template v-slot:default>
        <p class="conversation">{{ constuctingMessage }}</p>
      </template>
    </q-chat-message>
    <!-- content -->
  </q-page>
</template>

<style>
.conversation {
  white-space: pre-line;
}
</style>

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

    },
    async continueWith(what) {
      this.constuctingMessage = ""
      this.assistantWriting = true
      let toStr = what.toString()
      let id = this.route.params.id
      let response = await client.continueStoryTeller(id, toStr)
      const reader = response.body.getReader()
      let that = this

      reader.read().then(function processText({ done, value }) {
        if (done) {
          that.conversations.push({
            role: "assistant",
            content: that.constuctingMessage
          })
          that.assistantWriting = false
          return;
        }
        var decoded = new TextDecoder().decode(value);
        const splitted = decoded.split(/\r?\n/);
        for (const stringIndex in splitted) {
          let string = splitted[stringIndex]
          try {
            let parsed = JSON.parse(string)
            that.constuctingMessage = that.constuctingMessage + parsed.content
            console.log(parsed)

          } catch (err) {

          }
        }

        return reader.read().then(processText);
      });

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

          } catch (err) {

          }
        }

        return reader.read().then(processText);
      });

    }
  },
  computed: {
    filteredConversations() {
      return this.conversations.filter((conversation) => {
        return conversation.role != "system"
      })
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
      store: store,
      ownNewMessage: ref(''),
      assistantWriting: ref(false),
      constuctingMessage: ref('')
    }
  }
}
</script>
