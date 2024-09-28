<template>
    <div class="song_edit">
      <div class="container">
          <h2>{{ sgd.songName }}</h2>
          <form @submit.prevent="submitForm" id="create-form" enctype="multipart/form-data">
            <div class="mb-3">
              <label for="exampleFormControlTextarea1" class="form-label">Lyrics :</label>
              <textarea v-model="sgd.lyrics" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label>Artist :</label>
              <input v-model="sgd.artist" type="text" name="artist_name" />
            </div>
            <div class="mb-3">
              <label>Genre :</label>
              <input v-model="sgd.sgenre" type="text" name="sgenre" />
            </div>
            <div class="mb-3">
              <label for="formFileSm" class="form-label">Upload Audio</label>
              <input type="file" @change="handleFileUpload" class="form-control" id="formFileSm" accept=".mp3">
            </div>
            <div>
              <input type="submit" value="Publish" class="btn btn-outline-success">
            </div>

          </form>
          <br>
          <router-link to="/creator" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>        </div>
      </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        sgd: {
          songName: '',
          lyrics: '',
          sgenre: '',
          artist: ''
        },
        audioFile: null
      };
    },
    created() {
      const id = this.$route.params.id;
      this.fetchData(id);
    },
    methods: {
      fetchData(id) {
        const apiUrl = `http://localhost:5000/user/${id}/s/edit`;  
        const accessToken = localStorage.getItem('access_token');
          axios.get(apiUrl, {
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
          })
          .then(response => {            
            if (Array.isArray(response.data) && response.data.length > 0) {              
              const songData = response.data[0];              
              this.sgd.songName = songData.song_name || '';
              this.sgd.lyrics = songData.lyrics || '';
              this.sgd.sgenre = songData.sgenre || '';
              this.sgd.artist = songData.artist_name || '';
            } else {
              console.error('Invalid response data:', response.data);
            }
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
      },
      submitForm() {
        const id = this.$route.params.id;
        let formData = new FormData();
        formData.append('data', JSON.stringify(this.sgd));
        formData.append('file', this.audioFile); 
        const accessToken = localStorage.getItem('access_token'); 
        axios.post(`http://localhost:5000/user/${id}/s/edit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
           Authorization: `Bearer ${accessToken}`,
        },})
          .then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.error('Error editing song:', error);
          });
      },
      handleFileUpload(event) {
        this.audioFile = event.target.files[0];
      }
    }
  };
  </script>
  
  <style>
  body {
    background-color: #f8f9fa;
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
  