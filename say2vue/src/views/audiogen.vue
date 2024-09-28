<template>
    <div class="Audio">
      <h1>Advanced Text to Audio Song Generator</h1>
      <textarea v-model="text" placeholder="Enter long-form text here"></textarea>
      <button @click="generateSong">Generate Song</button>
      <audio v-if="audioSrc" :src="audioSrc" controls></audio>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        text: '',
        audioSrc: null,
      };
    },
    methods: {
      async generateSong() {
        try {
          const response = await axios.post('http://localhost:5000/generate', { text: this.text });
          this.audioSrc = `http://localhost:5000${response.data.audio_url}`;
        } catch (error) {
          console.error('Error generating song:', error);
        }
      }
    }
  }
  </script>
  