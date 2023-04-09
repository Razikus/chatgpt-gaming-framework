<template>
  <q-page padding>
    <q-chat-message v-bind:key="index" v-for="(conversation, index) in filteredConversations" :name="conversation.role"
      :avatar="conversation.role == 'assistant' ? assistentImage : playerImage" :text="[conversation.content]" :sent="conversation.role != 'assistant'" size="6" >
      <template v-slot:default>
        <p class="conversation">{{ conversation.content }}</p>
      </template>
    </q-chat-message>
    <q-chat-message name="You" avatar="~assets/player.png" size="6" sent v-if="!assistantWriting">
      <template v-slot:default>
        <div>
          Choose:
          <q-btn color="black" @click="continueWith('1)')">1)</q-btn>
          <q-btn color="black" @click="continueWith('2)')" style="margin-left: 5px">2)</q-btn>
          <q-btn color="black" @click="continueWith('3)')" style="margin-left: 5px">3)</q-btn>
          <div style="margin-top: 10px">
            Or write your own answer:
            <q-input ref="maininput" placeholder="Your own answer ..." class="blackinput" @keyup.enter="continueWith(ownNewMessage)" v-model="ownNewMessage"></q-input>

          </div>
        </div>
      </template>
    </q-chat-message>
    <q-chat-message name="assistant" avatar="~assets/download.png" size="6" v-else>
      <template v-slot:default>
        <p class="conversation">{{ constuctingMessage }}</p>
      </template>
    </q-chat-message>

    <q-dialog v-model="seamless" seamless position="bottom">
      <q-card style="width: 350px; margin-left: 0px; margin-right:auto; ">
        <q-linear-progress :value="musicProgress" color="pink" />

        <q-card-section class="row items-center no-wrap">
          <div>
            <div class="text-weight-bold">Story music</div>
          </div>

          <q-space />

          <q-btn flat :disabled="played" round @click="playMusic" icon="play_arrow" />
          <q-btn flat :disabled="!played" round @click="stopMusic" icon="pause" />
          <q-btn flat round @click="stopMusic" icon="close" v-close-popup />
        </q-card-section>
      </q-card>
    </q-dialog>
    <!-- content -->
  </q-page>
</template>

<style>
.conversation {
  white-space: pre-line;
}
.blackinput input {
  color: rgb(40, 39, 39) !important; 
  
}
</style>

<script>


import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { useMainStore } from 'stores/example-store';
import { client } from '../boot/axios'

export default {
  // name: 'PageName',
  watch: {
    $route(to, from) {
      this.loadStory()
    }
  },
  methods: {
    async loadStory() {

      let storyTellerOptions = await client.getStoryTellerOptions(this.route.params.id)
      let conversations = await client.getConversation(this.route.params.id)
      this.storyTeller = storyTellerOptions.data
      this.conversations = conversations.data.conversations

    },
    playMusic() {
      if(this.playedMusic == undefined ) {
        let audio = new Audio(this.storyTeller.metadata.music);
        audio.addEventListener("timeupdate", (ev) => {
          this.musicProgress = audio.currentTime / audio.duration
        })
        this.playedMusic = audio
      }
      this.played = true
      this.playedMusic.play()


    },
    stopMusic() {
      this.playedMusic.pause()
      this.played = false
    },
    async continueWith(what) {
      this.conversations.push({
        role: "user",
        content: what
      })

      this.ownNewMessage = ""
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
          that.$nextTick(() => {
            window.scrollTo(0, document.body.scrollHeight);
            that.$refs.maininput.focus()
          })
          return;
        }
        var decoded = new TextDecoder().decode(value);
        const splitted = decoded.split(/\r?\n/);
        for (const stringIndex in splitted) {
          let string = splitted[stringIndex]
          try {
            let parsed = JSON.parse(string)
            that.constuctingMessage = that.constuctingMessage + parsed.content

          } catch (err) {

          }
        }
        window.scrollTo(0, document.body.scrollHeight);


        return reader.read().then(processText);
      });

    },
    async createNewStory() {
      this.constuctingMessage = ""
      this.storyTeller = this.store.currentStory
      this.assistantWriting = true
      let response = await client.startStoryteller(this.store.currentStory)
      const reader = response.body.getReader()
      let that = this
      let uuidOfConversation = undefined

      reader.read().then(function processText({ done, value }) {
        if (done) {
          that.conversations.push({
            role: "assistant",
            content: that.constuctingMessage
          })
          that.assistantWriting = false
          that.router.push("/story/" + uuidOfConversation)
          return;
        }
        var decoded = new TextDecoder().decode(value);
        const splitted = decoded.split(/\r?\n/);
        for (const stringIndex in splitted) {
          let string = splitted[stringIndex]
          try {
            let parsed = JSON.parse(string)
            if (parsed.type == "stop") {
              uuidOfConversation = parsed.content
              let conversations = window.localStorage.getItem("conversations")
              if (conversations == null) {
                window.localStorage.setItem("conversations", JSON.stringify([uuidOfConversation]))
              } else {
                let parsedConv = JSON.parse(conversations)
                parsedConv.push(uuidOfConversation)
                window.localStorage.setItem("conversations", JSON.stringify(parsedConv))
              }
            } else {
              that.constuctingMessage = that.constuctingMessage + parsed.content
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
    const router = useRouter()
    const store = useMainStore()
    return {
      route: route,
      router: router,
      playerImage: playerImage,
      assistentImage: assistentImage,
      conversations: ref([]),
      storyTeller: ref({}),
      store: store,
      ownNewMessage: ref(''),
      assistantWriting: ref(false),
      constuctingMessage: ref(''),
      seamless: ref(true),
      played: ref(false),
      playedMusic: ref(undefined),
      musicProgress: ref(0.0)
    }
  }
}
</script>
