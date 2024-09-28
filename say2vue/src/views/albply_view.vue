<template>
    <div class="albply">
      <div class="nav-bar">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
          <div class="container-fluid">
            <a class="navbar-brand" href="#">MusPlay</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link to="/user_creator/1" class="nav-link">User</router-link>
              </li>
              <li v-if="role==='creator'" class="nav-item">
                <router-link to="/creator" class="nav-link">Creator</router-link>
              </li>
            </ul>
            </div>
          </div>
        </nav>
      </div>
      <br><br><br>
      <div class="text-center">
        <h3>{{ album_name.album_name }}</h3>
      </div>
      <div v-if="songs" class="main-body">
        <div class="songs">
          <div class="container text-center">
            <h6> Songs </h6>
            <div class="row">
              <div v-for="i in songs" :key="i.song_id" class="col">
                <div class="card" style="width: 18rem;">
                  <div class="card-body">
                    <img src="../assets/song_dis.png" class="card-img-top" alt="...">
                    <h5 class="card-title">{{ i.song_name }}</h5>
                    <h6>{{ i.artist_name }}</h6>
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
                    <router-link class="btn btn-outline-success" :to="`/song/${i.song_id}/1/add`"  tabindex="-1" role="button" aria-disabled="true">View</router-link>&nbsp;
                    <template v-if=" i.artist === this.creator_id">
                    <button v-if="role==='creator'" @click="deletions(album_name.album_name, 'als' + i.song_id)" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                    </template>                   
                    <button v-if="role==='user' || role==='creator'"  @click="deletions(album_name.album_name, 'pls' + i.song_id)" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                    </div>
                  </div>
                <br>
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
        selectedRate: '', 
        songs:null,
        album_name:'',
        code:'',
        role: (JSON.parse(localStorage.getItem('user')).role)[0],
        creator_id: (JSON.parse(localStorage.getItem('user')).user_id).toString()
      };
    },
    created() {                            
            this.fetchResource();                    
            },
    methods: {
            rateSong(id,value) {
            const formData = {
                rate: value,
             };
            const apiUrl = `http://localhost:5000/user_creator/${id}`;
            const accessToken = localStorage.getItem('access_token');
            axios.post(apiUrl, formData,{
                      headers: {
                          Authorization: `Bearer ${accessToken}`,
                      },
                  })
                .then(response => {
                 console.log(response.data);
                 this.fetchResource();
               })
                .catch(error => {
                console.error('Error submitting form:', error);                
                });            
            },
            deletions(id,code) {             
                const apiUrl = `http://localhost:5000//user/${id}/${code}/delete`;
                const accessToken = localStorage.getItem('access_token');     
                axios.get(apiUrl,{
                        headers: {
                            Authorization: `Bearer ${accessToken}`,
                        },
                    })
                    .then(response => {
                        this.fetchResource();
                        console.log('Fetched data:', response.data);
                        console.log('Fetched data:', code);
                    })
                    .catch(error => {
                    console.error('Error fetching data:', error);
                    });
          },
            fetchResource() { 
                const id = this.$route.params.id;
                const value = this.$route.params.value;     
                const apiUrl = `http://localhost:5000//album/${id}/${value}/view`;
                const accessToken = localStorage.getItem('access_token');      
                axios.get(apiUrl,
                  {
                      headers: {
                          Authorization: `Bearer ${accessToken}`,
                      },
                  })
                .then(response => {
                this.songs = response.data[0], 
                this.album_name = response.data[1],
                this.code = response.data[2]          
             console.log('Fetched data:', response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
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
  