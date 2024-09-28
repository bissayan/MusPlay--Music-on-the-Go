<template>
  <div class="song_create">
    <div class="container">
      <div class="login-container">
        <h2>Song on MusPlay</h2>
        <form @submit.prevent="createSong" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Song Name :</label>
            <input v-model="song.songName" type="text" class="form-control" id="song_name" placeholder="Song Name" required>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">Lyrics :</label>
            <textarea v-model="song.lyrics" class="form-control" id="lyrics" rows="5" cols="10"></textarea>
          </div>
          <br>
          <div>
            <label>Genre :</label>
            <input v-model="song.sgenre" type="text" name="sgenre">
          </div>
          <br>
          <div class="mb-3">            
            <label for="formFileSm" class="form-label">Upload Audio</label>
            <input type="file" @change="onFileSelected" accept=".mp3,.mp4">
          </div>
          <div>
            <button type="submit" class="btn btn-primary">Publish</button>
          </div>
        </form>
        <router-link to="/creator" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return { song: {
      songName: '',
      lyrics: '',
      sgenre: ''
    },    
      audioFile: null,
  }} ,
  methods: {
    createSong() {
      let formData = new FormData();
      formData.append('data',JSON.stringify(this.song))
      formData.append('file', this.audioFile);
      const accessToken = localStorage.getItem('access_token');
      axios.post('http://localhost:5000/song/create', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
         Authorization: `Bearer ${accessToken}`,
      },})
      .then(response => {
          console.log(response.data);
          this.$router.push('/creator');
        })
        .catch(error => {
          console.error('Error creating song:', error);
        });
    },
    onFileSelected(event) {
      this.audioFile = event.target.files[0];
      console.log(this.audioFile);
    },
  },
};
</script>

<style>
.song_create {
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

