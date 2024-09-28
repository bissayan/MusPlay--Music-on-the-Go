<template>
    <div class="album_edit">
      <div class="container">
        <h2>{{ album.albumName }}</h2>
        <form @submit.prevent="submitForm" id="create-form">            
          <div class="mb-3">
            <label>Album Name:</label>
            <input v-model="album.album_name" type="text" name="album_name" />
          </div>            
          <button type="submit" class="btn btn-primary">Save</button>
        </form>
        <br>
        <router-link to="/creator" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        album: {
            albumName:'',
        },
      };
    },
    created() {
      const id = this.$route.params.id;
      this.fetchData(id);
    },
    methods: {
      fetchData(id) {
        const apiUrl = `http://localhost:5000/user/${id}/alb/edit_album`;  
        const accessToken = localStorage.getItem('access_token');
          axios.get(apiUrl, {
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
          })
          .then(response => {      
            if (Array.isArray(response.data) && response.data.length > 0) {              
              const albuM = response.data[0]
              this.album.albumName = albuM.album_name;
              console.log('Fetched data:', response.data);
            } 
            else {
              console.error('Error: Invalid response data format');
            }
        })
    .catch(error => {
      console.error('Error fetching data:', error);
    })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
      },
      submitForm() {
        const id = this.$route.params.id;
        const formData = { 
          album_name: this.album.album_name,
        };      
        const accessToken = localStorage.getItem('access_token');
        axios.post(`http://localhost:5000/user/${id}/alb/edit_album`, formData,{
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
          })
          .then(response => {
            console.log(response.data);
            this.$router.push('/creator');
          })
          .catch(error => {
            console.error('Error editing album:', error);
          });
      }      
    }
  };
  </script>
  
  <style>
  body {
    background-color: #f8f9fa;
    font-family: 'Arial', sans-serif;
  }
  
  .container {
    max-width: 700px;
    margin: 50px auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s;
  }
  
  .container:hover {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  }
  
  .container h2 {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .btn {
    margin-top: 20px;
  }
  </style>
  