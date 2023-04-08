import { defineStore } from 'pinia';

export const useMainStore = defineStore('mainstore', {
  state: () => ({
    storyToCreate: {}
  }),
  getters: {
    currentStory: (state) => state.storyToCreate
  },
  actions: {
    setCurrentStory(story) {
      this.storyToCreate = story;
    }
  },
});
