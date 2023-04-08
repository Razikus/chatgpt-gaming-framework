<template>
  <div class="q-pa-lg">
    <div class="row q-pa-md">
      <div class="col-6 q-pa-md">
        World settings:
        <q-input filled v-model="year" label="World year" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />
        <q-input filled v-model="shortStory" type="textarea" label="World short story" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />
        <q-input filled v-model="playerRole" label="Player role" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />
        <q-input filled v-model="assistantRole" label="Assistant (AI) role" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />

        <q-select filled v-model="playerShortCharacteristics" use-input use-chips multiple
          hint="Player short characteristics" @new-value="createPlayerShortCharacteristic"
          :options="playerShortCharacteristicsOptions" />
        <q-input filled v-model="mainGoal" label="Main goal of the game" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />
      </div>
      <div class="col-6 q-pa-md">
        Rules:

        <q-select filled v-model="rules" use-input use-chips multiple hint="Game rules" @new-value="createRuleOption"
          :options="rulesOptions" />

        <q-input type="textarea" filled v-model="endingRule" label="Prompt ending rule" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type something']" />

        Metadata:

        <q-input filled v-model="musiclink" label="Music link" lazy-rules
          :rules="[val => val && val.length > 10 || 'Please type something']" />
        <q-btn color="green" @click="startTheStory"> Begin your story!</q-btn>
      </div>
    </div>

  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'

import { useMainStore } from 'stores/example-store';
import { useRouter } from 'vue-router'

let defaultRules = ["Progression should be slow, so the player can get to know the world and the characters.",
  "The goal should not be straighforward - not all actions should let into main goal",
  "Don't allow user to do impossible things and something unrelated to the story.",
  "Do not end the story",
  "Player should not be immediately informed about main goal"]

let shortCharacteristics = [
  "poor fisherman child",
  "often telling some jokes"
]

export default defineComponent({
  name: 'NewGamePage',
  methods: {
    createPlayerShortCharacteristic(value, done) {
      this.playerShortCharacteristicsOptions.push(value)
      done(value, 'toggle')
    },
    createRuleOption(value, done) {
      this.rulesOptions.push(value)
      done(value, 'toggle')
    },
    async startTheStory() {
      let convertedRules = []
      let convertedCharactersistics = []

      for (let i = 0; i < this.rules.length; i++) {
        convertedRules.push({
          "description": this.rules[i]
        })
      }
      for (let i = 0; i < this.playerShortCharacteristics.length; i++) {
        convertedCharactersistics.push(this.playerShortCharacteristics[i])
      }

      let req = {
        "storyTellerOptions": {
          "rules": convertedRules,
          "endingRule": {
            "description": this.endingRule
          },
          "world": {
            "year": this.year,
            "shortStory": this.shortStory,
            "playerRole": this.playerRole,
            "assistantRole": this.assistantRole,
            "playerShortCharacteristic": convertedCharactersistics,
            "mainGoal": this.mainGoal
          }
        },
        "metadata": {
          "music": this.musiclink
        }
      }
      await this.store.setCurrentStory(req)
      this.router.push({"path": "/story"})
    }
  },
  setup() {
    const store = useMainStore()
    const router = useRouter()
    
    return {
      store: store,
      router: router,
      year: ref("1876"),
      shortStory: ref(`The story should be about young boy Jack who wants to be a king of Atlantis.
The player is a boy who lives still on the earth but sometimes sees an mermaid looking at his boat, but immediately hides.
Nobody know that, but mermaids are forbidden to talk with humans.`),
      playerRole: ref(`player`),
      assistantRole: ref(`narrator`),
      mainGoal: ref(`Become a king of Atlantis`),
      playerShortCharacteristicsOptions: ref(shortCharacteristics),
      playerShortCharacteristics: ref(shortCharacteristics),
      endingRule: ref(`At the end always type a suggested possible short actions to do in format:
1) description of action 1
2) description of action 2
3) description of action 3
It should also contains only one set of action`),
      rules: ref(defaultRules),
      musiclink: ref("https://gptgames.s3.eu-central-1.amazonaws.com/pirate.mp3"),
      rulesOptions: ref(defaultRules)

    }
  }
})
</script>
