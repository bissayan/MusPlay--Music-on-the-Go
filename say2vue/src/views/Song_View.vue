<template>
    <div class ="song_view">
        <div class="container">        
          <div v-if="song">
            <h2>{{ song.song_name }}</h2>
            <p>
                <audio controls style="width: 220px;">
                  <source :src="song.sofile_id" type="audio/mpeg">
                </audio>
            </p>
            <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">Lyrics :</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="10" disabled>{{ song.lyrics }}</textarea>
            </div>
    
          <div v-if="val == 2">
            <div v-if="albums.length != 0">
              <form @submit.prevent="addToAlbum" id="add-form">
                  <div class="d-flex align-items-center"> 
                      <div class="flex-grow-1 me-3">
                          <label for="album" class="form-label">Select Album to Add to:</label>
                          <select v-model="selectedAlbum" name="album" id="album" class="form-select">
                              <option v-for="album in albums" :value="album.album_id">{{ album.album_name }}</option>
                          </select>
                      </div>
                      <button type="submit" class="btn btn-success">Add</button> 
                  </div>
                  <div>
                      <br>                    
                      <router-link to="/creator" class="btn btn-outline-primary">Go back</router-link>
                      <a v-if="song.value == 2" href="/user/{{ song.song_id }}/sl/delete" class="btn btn-outline-danger" tabindex="-1" role="button" aria-disabled="true">Delete lyrics</a>
                      <button v-if="song.value == 2" @click="edited()" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Edit</button>
                  </div>
              </form>

                </div>
            <div v-else>
                <br>
                <h6>You do not have an Album. Create Now!</h6>
                <router-link to="/creator" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
                <router-link to="/album/create" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Create an Album</router-link>
            </div>
            </div>
    
          <div v-else>
            <div v-if="playlists.length != 0">
              <form @submit.prevent="addToPlaylist" id="add-form">
                <div class="d-flex align-items-center"> 
                    <div class="flex-grow-1 me-3">
                        <label for="playlist" class="form-label">Select Playlist to Add to:</label>
                        <select v-model="selectedPlaylist" name="playlist" id="playlist" class="form-select">
                            <option v-for="playlist in playlists" :value="playlist.playlist_id">{{ playlist.playlist_name }}</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-success">Add</button> 
                </div>
                <router-link to="/user_creator/1" class="btn btn-outline-primary">Go back</router-link> 
            </form>

            </div>
            <div v-else>
                <br>
                <h6>You do not have a Playlist. Create Now!</h6>
                <router-link to="/user_creator/1" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Go back</router-link>
                <router-link to="/playlist/create" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Create a Playlist</router-link>
            </div>
            </div>
        </div>
        </div>        
        </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {    
    data() {
      return {
        song:null,
        albums:'',
        selectedAlbum: '', 
        selectedPlaylist: '', 
        playlists:'',         
      };
    },
    created() {
        const id=this.$route.params.song_id
        this.fetchData(id);
        console.log(this.$route.params);      
    },
    methods: {
      addToAlbum() {        
                    const code = this.selectedAlbum + "::" + this.$route.params.song_id;        
                    const accessToken = localStorage.getItem('access_token');
                    const apiUrl = `http://localhost:5000/song/${code}/2/add`;
                    axios.post(apiUrl, null, {
                      headers: {
                        Authorization: `Bearer ${accessToken}`,
                      },
                    })
                    .then(response => {                  
                      console.log('Song successfully added to the album');
                      this.$router.push('/creator');
                    })
                    .catch(error => {          
                      console.error('Error adding song to album:', error);
                    });
      },
      addToPlaylist() {        
            const code = this.selectedPlaylist + "::" + this.$route.params.song_id;
            console.log('Adding to playlist', this.selectedPlaylist);
            const accessToken = localStorage.getItem('access_token');
            const apiUrl = `http://localhost:5000/song/${code}/1/add`; 
            axios.post(apiUrl, null, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            })
            .then(response => {                  
              console.log('Song successfully added to the playlist');
              this.$router.push('/user_creator/1');
            })
            .catch(error => {          
              console.error('Error adding song to playlist:', error);
            });
          },

      edited() {
        const id=this.$route.params.song_id
        this.$router.push(`/user/${id}/s/edit`);      
    },      
      fetchData(id) {
          const value=this.$route.params.value
          const apiUrl = `http://localhost:5000/song/${id}/${value}/add`;
          this.val=value      
          const accessToken = localStorage.getItem('access_token');
          axios.get(apiUrl, {
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
          })
        .then(response => {
          this.song = response.data[0]
          if ( value==2){
            this.albums = response.data[1];
          }
          else{
            this.playlists = response.data[1];
          }          
          console.log('Fetched data:', response.data);
        })
        .catch(error => {          
          console.error('Error fetching data:', error);
        });
      },
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
  