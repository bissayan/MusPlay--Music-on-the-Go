<template>
    <div class="album_create">
      
        <div class="login-container">
          <h2>Album on MusPlay</h2>
  
          <form @submit.prevent="createAlbum" id="create-form">
            <div class="form-group">
              <label for="album_name">Album Name:</label>
              <input v-model="album_name" type="text" name="album_name" required>
            </div>
            <br>            
            <br>
            <div class="form-group">
              <label for="agenre">Genre:</label>
              <input v-model="agenre" type="text" name="agenre">
            </div>
            <br>
            <div class="form-group">
              <input type="submit" value="Create Album" class="btn btn-primary">
              <router-link to="/creator" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
            </div>
          </form>
        </div>
      </div>
   
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        album_name: '',        
        agenre: '',
      };
    },
    methods: {
      createAlbum() {
        const formData = {
          album_name: this.album_name,
          artist: this.artist,
          agenre: this.agenre,
        };
        const accessToken = localStorage.getItem('access_token');  
        axios.post('http://localhost:5000/album/create', formData,{
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
          })
          .then(response => {
            console.log(response.data);
            this.$router.push('/creator');
          })
          .catch(error => {
            console.error('Error creating album:', error);
          });
      },
    },
  };
  </script>
  
  <style>
    body {
      background-color: #faf8f8;
      font-family: 'Arial', sans-serif;
    }
  
    .login-container {
      max-width: 700px;
      margin: 50px auto;
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      transition: box-shadow 0.3s;
    }
  
    .login-container:hover {
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
    }
  
    .login-container h2 {
      text-align: center;
      margin-bottom: 30px;
    }
  </style>
  