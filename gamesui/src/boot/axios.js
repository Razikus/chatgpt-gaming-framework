import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: 'http://localhost:8000' })

class APIClient {
  constructor() {
    this.api = api
    this.apiurl = 'http://localhost:8000'
  }

  async startStoryteller(options) {
    const response = await fetch(this.apiurl + "/storyteller/start", {method: "POST", body: JSON.stringify(options), headers: {
      "Content-Type": "application/json",
    },})
    return response
  }

  async continueStoryTeller(id, text) {
    let options = {
      "id": id,
      "content": text
    }
    const response = await fetch(this.apiurl + "/storyteller/continue", {method: "POST", body: JSON.stringify(options), headers: {
      "Content-Type": "application/json",
    },})
    return response
  }

  async getConversation(idOf) {
    return await this.api.post(this.apiurl + "/storyteller/getConversation", {"id": idOf})
  }

  async getStoryTellerOptions(idOf) {
    return await this.api.post(this.apiurl + "/storyteller/getForConversation", {"id": idOf})
  }

}

const client = new APIClient()

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api

  app.config.globalProperties.$storytellerapi = client
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { client }
