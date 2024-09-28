<template>
    <div class="search">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">MusPlay</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link :to="'/policy'" class="nav-link">Policy</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="'/user_creator/1'" class="nav-link">User</router-link>
              </li>
              <li class="nav-item" v-if="role=== 'creator'">
                <router-link :to="'/creator'" class="nav-link">Creator</router-link>
              </li>
              <li class="nav-item" v-if="role=== 'admin'">
                <router-link to="/api/admin" class="nav-link">Dashboard</router-link>
              </li>
              <li class="nav-item" v-if="role=== 'admin'">
                <router-link to="/admin_support" class="nav-link">Support</router-link>
              </li>
            </ul>
            <form  method="GET" class="d-flex" role="search" @submit.prevent="search">              
              <input v-model="searchRequest" class="form-control me-2" type="text" name="search_request" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>            
            <button @click="logout()" class="btn btn-outline-primary" tabindex="-1" role="button">LogOut</button>
          </div>
        </div>
      </nav>  
      <!-- Display of Search Query -->
      <h2 v-if="query">You Searched for: {{ query }}</h2>      
      <div v-if="songNamesMatched" class="main-body">
        <div class="songs">            
          <div class="container text-center">
            <div class="row">
              <h6>Songs</h6>
              <div v-for="i in songNamesMatched" :key="i.song_id" class="col">
                <div class="card" style="width: 18rem;">
                  <img src="..\assets\song_dis.png" class="card-img-top" alt="...">
                  <div class="card-body">
                    <h4 class="card-title">{{ i.song_name }}</h4>
                    <h5>{{ i.artist_name }}</h5>
                    <h6 v-if="i.rating !== null">{{ i.rating }} Stars</h6>
                    <h6 v-else>No Ratings Yet</h6>
                    <p><audio controls style="width: 220px;">
                        <source :src="i.sofile_id" type="audio/mpeg">
                    </audio></p>
                    <template>
                      <form v-if=" i.artist !== this.creator_id" @submit.prevent="rateSong(i.song_id, i.selectedRating)">
                      <div class="rating-stars" style="display: flex; justify-content: center; flex-direction: row-reverse;">
                        <input type="radio" :id="`star5_${i.song_id}`" :name="`rate_${i.song_id}`" value="5" v-model="i.selectedRating">
                        <label :for="`star5_${i.song_id}`" title="5 stars"></label>
                        <input type="radio" :id="`star4_${i.song_id}`" :name="`rate_${i.song_id}`" value="4" v-model="i.selectedRating">
                        <label :for="`star4_${i.song_id}`" title="4 stars"></label>
                        <input type="radio" :id="`star3_${i.song_id}`" :name="`rate_${i.song_id}`" value="3" v-model="i.selectedRating">
                        <label :for="`star3_${i.song_id}`" title="3 stars"></label>
                        <input type="radio" :id="`star2_${i.song_id}`" :name="`rate_${i.song_id}`" value="2" v-model="i.selectedRating">
                        <label :for="`star2_${i.song_id}`" title="2 stars"></label>
                        <input type="radio" :id="`star1_${i.song_id}`" :name="`rate_${i.song_id}`" value="1" v-model="i.selectedRating">
                        <label :for="`star1_${i.song_id}`" title="1 star"></label>
                      </div>
                      <button type="submit" class="btn btn-outline-success">Rate</button>
                    </form>
                    </template>
                    <router-link :to="'/song/' + i.song_id + '/1/add'" class="btn btn-outline-success" tabindex="-1" role="button" aria-disabled="true">View</router-link>&nbsp;
                    <template v-if="role=== 'admin'">
                      <button v-if="i.soflag != 1" @click="actions('s', i.song_id)" class="btn btn-outline-primary" tabindex="-1" role="button">Flag</button>   
                       &nbsp;
                       <button v-if="i.soflag == 1" @click="actions('ufs', i.song_id)" class="btn btn-outline-success" tabindex="-1" role="button">UnFlag</button>
                        &nbsp;
                      <button @click="deletions(i.song_id,'slad' )" class="btn btn-outline-warning" tabindex="-1" role="button">Delete Lyris</button>
                       &nbsp;
                      <button @click="deletions(i.song_id,'sfad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                    </template>
                    <template v-if="role=== 'creator'">
                      <button v-if="i.soflag != 1 &&  i.artist === this.creator_id" @click="edited(i.song_id,'s')" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Edit</button>
                      &nbsp;
                      <button v-if="i.soflag != 1 &&  i.artist === this.creator_id" @click="deletions(i.song_id,'sf' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                    </template>
                    <h6 v-if="i.artist === this.creator_id && i.soflag == 1">Flagged</h6>
                  </div>
                </div>
                <br>
              </div>
            </div>
          </div>
        </div>
      </div>  
      <!-- Artist Cards -->
      <div v-if="artistNamesMatched" class="container">
        <h6>Artists</h6>
        <div class="row">
          <div v-for="artist in artistNamesMatched" :key="artist.id" class="col">
            <div class="card" style="width: 18rem;">
                <img src="..\assets\artist_dis.png" class="card-img-top" alt="...">              
              <div class="card-body">
                <h5 class="card-title">{{ artist.user_name }}</h5>
                <template v-if="role=== 'admin'">
                    <button @click="actions('u', artist.artist)" class="btn btn-outline-primary" tabindex="-1" role="button">Flag</button>                       
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>  
      <!-- Albums Section -->
      <div v-if="albumNamesMatched" class="container">
        <h6>Albums</h6>
        <div class="row">
          <div v-for="album in albumNamesMatched" :key="album.album_id" class="col">
            <div class="card" style="width: 18rem;">              
              <div class="card-body">
                <h5 class="card-title">{{ album.album_name }}</h5>
                <img src="../assets/alb_dis.png" class="card-img-top" alt="...">
                <router-link :to="'/album/' + album.album_id + '/1/view'" class="btn btn-outline-success">Open</router-link>&nbsp;              
                <template v-if="role!== 'user'">
                  <button v-if="role=== 'admin' || album.artist === this.creator_id" @click="deletions(album.album_id,'albad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>  
      <!-- Genre Songs Section -->
      <div v-if="genreSongsMatched" class="container">
        <h6>Genre Songs</h6>
        <div class="row">
          <div v-for="i in genreSongsMatched" :key="i.song_id" class="col">
            <div class="card" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">{{ i.song_name }}</h5>
                <img src="..\assets\song_dis.png" class="card-img-top" alt="...">                  
                    <h5>{{ i.artist_name }}</h5>
                    <h6 v-if="i.rating !== null">{{ i.rating }} Stars</h6>
                    <h6 v-else>No Ratings Yet</h6>
                    <p><audio controls style="width: 220px;">
                        <source :src="i.sofile_id" type="audio/mpeg">
                    </audio></p>
                    <template>
                      <form v-if=" i.artist !== this.creator_id" @submit.prevent="rateSong(i.song_id, i.selectedRating)">
                      <div class="rating-stars" style="display: flex; justify-content: center; flex-direction: row-reverse;">
                        <input type="radio" :id="`star5_${i.song_id}`" :name="`rate_${i.song_id}`" value="5" v-model="i.selectedRating">
                        <label :for="`star5_${i.song_id}`" title="5 stars"></label>
                        <input type="radio" :id="`star4_${i.song_id}`" :name="`rate_${i.song_id}`" value="4" v-model="i.selectedRating">
                        <label :for="`star4_${i.song_id}`" title="4 stars"></label>
                        <input type="radio" :id="`star3_${i.song_id}`" :name="`rate_${i.song_id}`" value="3" v-model="i.selectedRating">
                        <label :for="`star3_${i.song_id}`" title="3 stars"></label>
                        <input type="radio" :id="`star2_${i.song_id}`" :name="`rate_${i.song_id}`" value="2" v-model="i.selectedRating">
                        <label :for="`star2_${i.song_id}`" title="2 stars"></label>
                        <input type="radio" :id="`star1_${i.song_id}`" :name="`rate_${i.song_id}`" value="1" v-model="i.selectedRating">
                        <label :for="`star1_${i.song_id}`" title="1 star"></label>
                      </div>
                      <button type="submit" class="btn btn-outline-success">Rate</button>
                    </form>
                    </template>
                    <router-link :to="'/song/' + i.song_id + '/1/add'" class="btn btn-outline-success" tabindex="-1" role="button" aria-disabled="true">View</router-link>&nbsp;
                    <template v-if="role=== 'admin'">
                      <button v-if="i.soflag != 1" @click="actions('s', i.song_id)" class="btn btn-outline-primary" tabindex="-1" role="button">Flag</button>   
                       &nbsp;
                      <button v-if="i.soflag == 1" @click="actions('ufs', i.song_id)" class="btn btn-outline-success" tabindex="-1" role="button">UnFlag</button>
                        &nbsp;
                      <button @click="deletions(i.song_id,'slad' )" class="btn btn-outline-warning" tabindex="-1" role="button">Delete Lyris</button>
                       &nbsp;
                      <button @click="deletions(i.song_id,'sfad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                   </template>
                    <template v-if="role=== 'creator'">
                      <button v-if="i.soflag != 1 &&  i.artist === this.creator_id" @click="edited(i.song_id,'s')" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Edit</button>
                       &nbsp;
                      <button v-if="i.soflag != 1 &&  i.artist === this.creator_id"  @click="deletions(i.song_id,'sf' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>                      
                    </template>
                    <h6 v-if="i.artist === this.creator_id && i.soflag == 1">Flagged</h6>
                  </div>
              </div>
            </div>
          </div>
        </div>   
      <!-- Genre Albums Section -->
      <div v-if="genreAlbumsMatched" class="container">
        <h6>Genre Albums</h6>
        <div class="row">
          <div v-for="album in genreAlbumsMatched" :key="album.album_id" class="col">
            <div class="card" style="width: 18rem;">              
              <div class="card-body">
                <h5 class="card-title">{{ album.album_name }}</h5>
                <img src="../assets/alb_dis.png" class="card-img-top" alt="..."> 
                <router-link :to="'/album/' + album.album_id + '/1/view'" class="btn btn-outline-success" tabindex="-1" role="button" aria-disabled="true">Open</router-link>&nbsp;              
                <template v-if="role!== 'user'">
                  <button v-if="role=== 'admin' || album.artist === this.creator_id" @click="deletions(album.album_id,'albad' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                </template>
              </div>
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
        code:null, 
        query: '', 
        songNamesMatched: null, 
        artistNamesMatched: null, 
        albumNamesMatched: null,
        genreSongsMatched: null, 
        genreAlbumsMatched: null, 
        searchRequest:null,
        role: (JSON.parse(localStorage.getItem('user')).role)[0],
        creator_id: (JSON.parse(localStorage.getItem('user')).user_id).toString()
      };
    },    
    created() {        
        const query = this.$route.params.query;
        this.search(query);
    },
    methods: {
      rateSong(id,value) {
                  const formData = {
                  rate: value,                    
            };
            const apiUrl = `http://localhost:5000/user_creator/${id}`;
            axios.post(apiUrl, formData)
              .then(response => {
                console.log(response.data);
                this.search();
              })
              .catch(error => {
                console.error('Error submitting form:', error);
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
              if(this.role=='admin'){
                  this.$router.push('/admin_support');
                }
                else {
                  this.$router.push('/creator');
                }
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
                if(this.role=='admin'){
                  this.$router.push('/admin_support');
                }
                else {
                  this.$router.push('/creator');
                }
                console.log('Fetched data:', response.data);
            })
            .catch(error => {
            console.error('Error fetching data:', error);
            });
        },
        edited(id,code) {
            if(code=='s'){        
               this.$router.push(`/user/${id}/${code}/edit`);
            }
            if(code=='alb'){
                this.$router.push(`/user/${id}/${code}/edit_album`);
        }
        },
    search(query) {
            query=this.searchRequest
            if (!query) {
                 query = this.$route.params.query;
                }
                
                const apiUrl = `http://localhost:5000/search/${query}`;
                const accessToken = localStorage.getItem('access_token');
                axios.get(apiUrl, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
            },
    })
    .then(response => {      
      const [genreAlbums, genreSongs, artists, songs, albums] = response.data;
      this.genreAlbumsMatched = genreAlbums;
      this.genreSongsMatched = genreSongs;
      this.artistNamesMatched = artists;
      this.songNamesMatched = songs;
      this.albumNamesMatched = albums;
      this.code='0';

      console.log('Fetched data:', response.data);
      //this.$router.push(apiUrl);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
},  logout(){    
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
},};
  </script>
  
  <style>
  .card {
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }

  .rating-stars input[type="radio"] {
  display: none;
}
.rating-stars label {
  font-size: 30px;
  color: #ddd;
  cursor: pointer;
}
.rating-stars label:hover,
.rating-stars label:hover ~ label {
  color: #ffc107;
}
.rating-stars input[type="radio"]:checked ~ label {
  color: #ffc107;
}
.rating-stars label::before {
  content: '\2605';
  margin-right: 5px;
}
  </style>
  