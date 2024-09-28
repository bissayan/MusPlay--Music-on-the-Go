<template>
    <div class="admin_support">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">MusPlay Admin Support</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link class="nav-link" :to="{ path: '/policy' }">Policy</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/api/admin">Dashboard</router-link>
              </li>       
            </ul>
            <form @submit.prevent="search" class="d-flex">
              <input v-model="searchRequest" class="form-control me-2" type="text" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            <button @click="logout()" class="btn btn-outline-primary" tabindex="-1" role="button">LogOut</button>             
          </div>
        </div>
      </nav>
  
      <br><br><br>
  
      <!-- Display flagged songs -->
      <div v-if="songNamesFlagged.length > 0" class="main-body">
        <div class="songs">
        <div v-if="songNamesFlagged && songNamesFlagged.length > 0"> 
          <div class="container text-center">
            <h6>Songs Flagged</h6>
            <div class="row">
              <div v-for="song in songNamesFlagged" :key="song.song_id" class="col">
                <div class="card" style="width: 18rem;">
                  <img src="../assets/song_dis.png" class="card-img-top" alt="...">
                  <div class="card-body">
                    <h4 class="card-title">{{ song.song_name }}</h4>
                    <h5>{{ song.artist_name }}</h5>
                    <h6 v-if="song.rating !== null">{{ song.rating }} Stars</h6>
                    <h6 v-else>No Ratings Yet</h6>
                    <p><audio controls style="width: 220px;">
                      <source :src="`../static/song_store/${song.sofile_id}`" type="audio/mpeg">
                    </audio></p>
                    <button @click="actions('ufs', song.song_id)" class="btn btn-outline-success" tabindex="-1" role="button">UnFlag</button>
                    &nbsp;
                    <button @click="deletions(song.song_id,'slad' )" class="btn btn-outline-warning" tabindex="-1" role="button">Delete Lyris</button>
                    &nbsp;                  
                    <button @click="deletions(song.song_id,'sfad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                  </div>
                </div>
                <br>
              </div>
            </div>
          </div>
         </div>
        </div>
      </div>
  
      <!-- Display flagged artists -->
      <div v-if="artistNamesFlagged.length > 0" class="artists">
        <div class="container text-center">
          <h6>Artists Flagged</h6>
          <div class="row">
            <div v-for="artist in artistNamesFlagged" :key="artist.id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="../assets/artist_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ artist.user_name }}</h5>
                  <button @click="actions('ufa', artist.artist)" class="btn btn-outline-success" tabindex="-1" role="button">WhiteList</button>
                  &nbsp;
                  <button @click="deletions(artist.artist,'uad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                </div>
              </div>
              <br>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Display matched songs -->
      <div v-if="songNamesMatched.length > 0" class="songs">
        <div class="container text-center">
          <h6>Songs</h6>
          <div class="row">
            <div v-for="song in songNamesMatched" :key="song.song_id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="../assets/song_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h4 class="card-title">{{ song.song_name }}</h4>
                  <h5>{{ song.artist_name }}</h5>
                  <h6 v-if="song.rating !== null">{{ song.rating }} Stars</h6>
                  <h6 v-else>No Ratings Yet</h6>
                  <p><audio controls style="width: 220px;">
                    <source :src="song.sofile_id" type="audio/mpeg">
                  </audio></p>
                  <button @click="actions('s', song.song_id)" class="btn btn-outline-primary" tabindex="-1" role="button">Flag</button>   
                  &nbsp;
                  <button @click="deletions(song.song_id,'slad' )" class="btn btn-outline-warning" tabindex="-1" role="button">Delete Lyris</button>
                  &nbsp;
                  <button @click="deletions(song.song_id,'sfad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                
                </div>
              </div>
              <br>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Display matched artists -->
      <div v-if="artistNamesMatched.length > 0" class="artists">
        <div class="container text-center">
          <h6>Artist</h6>
          <div class="row">
            <div v-for="artist in artistNamesMatched" :key="artist.id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="../assets/artist_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ artist.user_name }}</h5>
                  <button @click="actions('u', artist.artist)" class="btn btn-outline-warning" tabindex="-1" role="button">BlackList</button>
                  &nbsp;                  
                  <button @click="deletions(artist.artist,'uad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                </div>
              </div>
              <br>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Display matched albums -->
      <div v-if="albumNamesMatched.length > 0" class="albums">
        <div class="container text-center">
          <h6>Albums</h6>
          <div class="row">
            <div v-for="album in albumNamesMatched" :key="album.album_id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="../assets/alb_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ album.album_name }}</h5>
                  <p>{{ album.artist_name }}</p>
                  <button @click="deletions(album.album_id,'albad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                </div>
              </div>
              <br>
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
      songNamesFlagged: [], 
      songNamesMatched: [],
      artistNamesFlagged: [], 
      artistNamesMatched: [],
      albumNamesMatched: [],
      searchRequest: '',       
      };
    },
    created() {                
            this.fetchData();                    
            },
    methods: {
      search() {
            let query=this.searchRequest
            this.$router.push('/search/' + query);
    },
    
    fetchData() {      
      const apiUrl = 'http://localhost:5000/admin_support'; 
      const accessToken = localStorage.getItem('access_token');     
      axios.get(apiUrl,{
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        })
        .then(response => {
          this.artistNamesFlagged = response.data[0];
          this.songNamesFlagged = response.data[1];
          this.artistNamesMatched = response.data[2];
          this.songNamesMatched = response.data[3];         
          this.albumNamesMatched = response.data[4];          
          
          console.log('Fetched data:', response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
      },
      actions(code,id) {             
        const apiUrl = `http://localhost:5000//flag_unflag/${code}/${id}`; 
        const accessToken = localStorage.getItem('access_token');     
        axios.get(apiUrl,{
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            })
            .then(response => {
                this.fetchData();
                console.log('Fetched data:', response.data);
            })
            .catch(error => {
            console.error('Error fetching data:', error);
            });
        },
        deletions(id,code) {             
        const apiUrl = `http://localhost:5000//user/${id}/${code}/delete`;
        const accessToken = localStorage.getItem('access_token');      
        axios.get(apiUrl, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            })
            .then(response => {
                this.fetchData();
                console.log('Fetched data:', response.data);
            })
            .catch(error => {
            console.error('Error fetching data:', error);
            });
        },
        logout(){    
          const accessToken = localStorage.getItem('access_token');
            axios.post(`http://localhost:5000/logout`, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            })
                .then(() => {                    
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('user');                    
                    this.$router.push("/api/login");
                    }
                )
                .catch(error => {
                    console.error('Logout failed:', error);
                });        
           },
    },
  };
  </script>
  
  <style>
  .card {
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  </style>
  