<template>
  <div class ="user_data">
     <div class="nav-bar">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/">MusPlay</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">              
              <li class="nav-item" v-if="role=== 'creator'">
                <router-link to="/creator" class="nav-link" tabindex="-1" role="button" aria-disabled="true">Creator</router-link>
              </li>
              <li class="nav-item" v-else>
                <button @click="creator_become()" class="nav-link" tabindex="-1" role="button" aria-disabled="true">Become Creator</button>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/playlist/create">Create a Playlist</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/policy">Policy</router-link>
              </li>
            </ul>
            <form  method="GET" class="d-flex" role="search" @submit.prevent="search">
              <input type="hidden" name="ID" value="2">
              <input v-model="searchRequest" class="form-control me-2" type="text" name="search_request" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>  
            <button @click="logout()" class="btn btn-outline-primary" tabindex="-1" role="button">LogOut</button>
          </div>
        </div>
      </nav>
    </div> 
    <!-- Songs -->
      <div v-if="songs && songs.length > 0" class="songs">
            <h6> Songs </h6>
            <div class="row">
              <div v-for="i in songs" :key="i.song_id" class="col">
                <div class="card" style="width: 18rem;">
                  <img src="../assets/song_dis.png" class="card-img-top" alt="...">
                  <div class="card-body">
                    <h4 class="card-title">{{ i.song_name }}</h4>
                    <h5>{{ i.artist_name }}</h5>
                    <h6 v-if="i.rating !== null">{{ i.rating }} Stars</h6>
                    <h6 v-else>No Ratings Yet</h6>
                    <p>
                      <audio controls style="width: 220px;">
                        <source :src="i.sofile_id" type="audio/mpeg">
                      </audio>
                    </p>                                     
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
                    <router-link class="btn btn-outline-success" :to="`/song/${i.song_id}/1/add`"  tabindex="-1" role="button" aria-disabled="true">View</router-link>
                  </div>
                </div>    
              <br>
            </div>
          </div>
        </div>
      

      <!-- Albums -->
      <div v-if="albums && albums.length > 0" class="albums">
        
          <h6> Albums </h6>
          <div class="row">
            <div v-for="j in albums" :key="j.album_id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="../assets/alb_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ j.album_name }}</h5>
                  <router-link :to="'/album/' + j.album_id + '/1/view'" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">View</router-link>
                </div>
              </div>
              <br>
            </div>
          </div>
        </div>
      

      <!-- Playlists -->
      <div v-if="playlists && playlists.length > 0" class="playlists">        
          <h6> Your Playlists</h6>
          <div class="row">
            <div v-for="j in playlists" :key="j.playlist_id" class="col">
              <div class="card" style="width: 18rem;">
                <img src="..\assets\ply_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ j.playlist_name }}</h5>
                  <router-link :to="'/album/' + j.playist_id + '/0/view'" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">View</router-link>
                  &nbsp;
                  <button @click="deletions(j.playlist_name,'xyz' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>               
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
      songs: null,
      albums: null,
      playlists: null,
      searchRequest: '',
      query:'',
      role: (JSON.parse(localStorage.getItem('user')).role)[0],
      creator_id: (JSON.parse(localStorage.getItem('user')).user_id).toString()
      
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
    rateSong(id, value) {
      const formData = {
        rate: value,
      };
      const apiUrl = `http://localhost:5000/user_creator/${id}`;
      const accessToken = localStorage.getItem('access_token');
      axios.post(apiUrl, formData, {
          headers: {
              Authorization: `Bearer ${accessToken}`,
          },
      })      
        .then(response => {
          console.log(response.data);
          this.fetchData();
        })
        .catch(error => {
          console.error('Error rating song:', error);
        });
    },
    
    creator_become() {
      const apiUrl = `http://localhost:5000/user/creator`;
      const accessToken = localStorage.getItem('access_token');
      axios.get(apiUrl, {
          headers: {
              Authorization: `Bearer ${accessToken}`,
          },
      })      
        .then(response => {
          console.log(response.data);
          this.logout();
        })
        .catch(error => {
          console.error('Error becoming Creator:', error);
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
    fetchData() {
      const apiUrl = `http://localhost:5000/user_creator/1`;
      const accessToken = localStorage.getItem('access_token');
      //const user = localStorage.getItem('user');
      axios.get(apiUrl, {
      headers: {
          Authorization: `Bearer ${accessToken}`,
      },
      })
        .then(response => {
          this.songs = response.data[0];
          this.albums = response.data[1];
          this.playlists = response.data[2];
          this.user = localStorage.getItem('user');
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