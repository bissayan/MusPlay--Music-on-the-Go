<template>
  <div class="admin_dashboard">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">MusPlay Admin</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/policy" class="nav-link">Policy</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin_support" class="nav-link">TrackAlbum</router-link>
            </li>
          </ul>
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
      </div>
      <div class="song_performance">
        <canvas ref="songGraphCanvas" width="400" height="200"></canvas>        
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
      monitor: {
        Users: 0,
        Creators: 0,
        Songs: 0,
        Albums: 0,
        Genres: 0
      },
      songNames: null,
      listens: null,
      chart: null
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      const apiUrl = 'http://localhost:5000/api/admin';
      const accessToken = localStorage.getItem('access_token');
      axios.get(apiUrl, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.monitor = response.data[0];
        this.songNames = response.data[1];
        this.listens = response.data[2];

        this.GraphPlotter();
        console.log('Fetched data:', response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
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
              backgroundColor: 'rgba(75,192,192,0.2)',
              borderColor: 'rgba(75,192,192,1)',
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
    logout() {
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
      })
      .catch(error => {
        console.error('Logout failed:', error);
      });
    },
  }
};
</script>

<style scoped>
.card1 {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
</style>