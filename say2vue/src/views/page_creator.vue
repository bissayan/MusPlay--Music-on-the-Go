<template>
    <div class="page_creator">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">MusPlay</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              
              <!-- User's name--> 
              <li class="nav-item">
                <h5 class="nav-link" >{{ user.user_name }}</h5>
              </li>
              <!-- Links to user-related pages -->
              <li class="nav-item">
                <a class="nav-link" href="/user_creator/1">User</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/song/create">Create a Song</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/album/create">Create an Album</a>
              </li>
              <!-- Policy link -->
              <li class="nav-item">
                <a class="nav-link" href="/policy">Policy</a>
              </li>
              <li class="nav-item">
              <button @click="CSV_Report" class="btn btn-outline-warning" tabindex="-1" role="button">DownLoad Reprort</button>
              </li>
            </ul>
            <!-- Search form -->
            <form  method="GET" class="d-flex" role="search" @submit.prevent="search">              
              <input v-model="searchRequest" class="form-control me-2" type="text" name="search_request" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            <button @click="logout()" class="btn btn-outline-primary" tabindex="-1" role="button">LogOut</button>
          </div>
        </div>
      </nav>
  
      
      <div class="container mt-5">
        <div class="row">
          <div class="col-md-4" v-for="(value, key) in monitor" :key="key">
            <div class="card1">
              <div class="card-body">
                <h2 class="card-title">{{ key }}</h2>
                <p class="card-text">{{ value }}</p>
              </div>
            </div>
          </div>
          <div class="song_performance">
            <canvas ref="songGraphCanvas" width="400" height="200"></canvas>
        </div>
        </div>
      
      <!-- Display user's songs -->
      <div v-if="songs" class="main-body">
        <div class="songs">
          <div class="container text-center">
            <h6>Your Songs</h6>
            <div class="row">              
              <div v-for="i in songs" :key="i.song_id" class="col">
                <div class="card" style="width: 18rem;">                  
                  <img src="../assets/song_dis.png" class="card-img-top" alt="...">
                  <div class="card-body">
                    <h4 class="card-title">{{ i.song_name }}</h4>
                    <h5>{{ i.artist_name }}</h5>
                    <h6 v-if="i.rating != null">{{ i.rating }} Stars</h6>
                    <h6 v-else>No Ratings Yet</h6>
                    <p>
                      <audio controls style="width: 220px;">
                        <source :src="i.sofile_id" type="audio/mpeg"></audio>
                    </p>                  
                    <router-link v-if="i.soflag != 1" class="btn btn-outline-success" :to="`/song/${i.song_id}/2/add`"  tabindex="-1" role="button" aria-disabled="true">View</router-link>
                    &nbsp;
                    <button v-if="i.soflag != 1" @click="edited(i.song_id,'s')" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Edit</button>
                    &nbsp;
                    <button v-if="i.soflag != 1"  @click="deletions(i.song_id,'sf' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>               
                    <h6 v-else>Flagged</h6>
                  </div>
                </div>
                <br>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Display user's albums -->
      <div v-if="albums" class="albums">
        <div class="container text-center">
          <h6>Your Albums</h6>
          <div class="row">            
            <div v-for="j in albums" :key="j.album_id" class="col">
              <div class="card" style="width: 18rem;">                
                <img src="../assets/alb_dis.png" class="card-img-top" alt="...">
                <div class="card-body">
                  <h5 class="card-title">{{ j.album_name }}</h5>
                  <router-link :to="'/album/' + j.album_id + '/1/view'" class="btn btn-outline-success" tabindex="-1" role="button" aria-disabled="true">Open</router-link>
                  &nbsp;
                  <button @click="deletions(j.album_id,'alb' )" class="btn btn-outline-danger" tabindex="-1" role="button">Delete</button>
                  &nbsp;
                  <button @click="edited(j.album_id,'alb')" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="true">Edit</button>
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
  import Chart from 'chart.js/auto';
  export default {
    data() {
      return {
        user:'',
        songs: null,
        albums: null,
        songNames: null,
        listens: null,
        chart: null
      };
    },
    created() {
      this.fetchCreator();
    },
    methods: {
        edited(id,code) {
            if(code=='s'){        
               this.$router.push(`/user/${id}/${code}/edit`);
            }
            if(code=='alb'){
                this.$router.push(`/user/${id}/${code}/edit_album`);
        }
        },
        CSV_Report(){
                      const accessToken = localStorage.getItem('access_token')
                      const headers= {
                            Authorization: `Bearer ${accessToken}`,
                        };                      
                      axios.post('http://localhost:5000/export/report',null,{
                        headers: headers,
                        responseType : 'blob',                       
                      })
                      .then(response => {
                      const downloadLink = document.createElement('a');
                      downloadLink.href =  URL.createObjectURL(response.data);
                      downloadLink.download = 'song_report.csv';
                      document.body.appendChild(downloadLink)
                      downloadLink.cick();
                      })
                    },
      deletions(id,code) {             
        const apiUrl = `http://localhost:5000/user/${id}/${code}/delete`; 
        const accessToken = localStorage.getItem('access_token')     
        axios.get(apiUrl, {
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
            })
            .then(response => {
                this.fetchCreator();
                console.log('Fetched data:', response.data);
            })
            .catch(error => {
            console.error('Error fetching data:', error);
            });
        },
        search() {
            let query=this.searchRequest     
            this.$router.push('/search/' + query);
        },
        GraphPlotter() {
      if (this.chart) {
        this.chart.destroy();
      }
      const ctx = this.$refs.songGraphCanvas.getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.songNames,
          datasets: [
            {
              label: 'Listens',
              data: this.listens,
              backgroundColor: 'rgba(0, 119, 190, 0.2)',
          borderColor: 'rgba(0, 119, 190, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },
        fetchCreator() {
          const apiUrl = `http://localhost:5000/creator`;
          const accessToken = localStorage.getItem('access_token');
          axios.get(apiUrl, {
              headers: {
                  Authorization: `Bearer ${accessToken}`,
              },
            })
          .then(response => {
            this.songs = response.data[0];
            this.albums = response.data[1];            
            this.monitor = response.data[2];
            this.user = response.data[3];
            this.songNames = response.data[4];
            this.listens = response.data[5]; 

            this.GraphPlotter();

            console.log(response.data)
            if(this.user.usflag=='1'){
                this.$router.push('/policy');
            }     
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
  .card1 {
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  </style>
  