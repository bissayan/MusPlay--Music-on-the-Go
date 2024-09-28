<template>
    <div class="playlist_create">
      <div class="login-container">
        <h2>Playlist on MusPlay</h2>
        <form @submit.prevent="createPlaylist" id="create-form">
          <div>
            <label>Playlist Name:</label>
            <input v-model="playlist_name" type="text" required />
          </div><br>
          <!--<div>
            <label>Artist:</label>
            <input type="text" :value="user.user_name" disabled />
          </div>-->
          <br>
          <div>
            <label>Genre:</label>
            <input v-model="pgenre" type="text" />
          </div><br>
          <div>
            <button type="submit" class="btn btn-outline-primary">Create Playlist</button>
            <router-link to="/user_creator/1" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
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
        playlist_name: '',
        pgenre: '',
      };
    },
    
    methods: {
      createPlaylist() {
        const formData = {
          playlist_name: this.playlist_name,          
          pgenre: this.pgenre,
        };
        const accessToken = localStorage.getItem('access_token');
        axios.post('http://localhost:5000/playlist/create', formData,{
              headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
          .then(response => {
            console.log(response.data);
            this.$router.push('/user_creator/1');
          })
          .catch(error => {
            console.error('Error creating album:', error);
            // Handle the error
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
  