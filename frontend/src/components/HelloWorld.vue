<template>
  <h3>{{message}}</h3>
</template>

<script>
/* eslint-disable */
  export default {
    name: 'HelloWorld',
    data() {
      return {
        message: ''
      }
    },
    methods: {
      async fetchMessage() {
        const response = await fetch('http://localhost:8000/api/v1/test/')
        this.message = await response.json()
        this.message = this.message['message']
      }
    },
    async created() {
      await this.fetchMessage()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
