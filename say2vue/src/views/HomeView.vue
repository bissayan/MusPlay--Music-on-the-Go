<template>
  <div class="home">
    <div class="hero">
      <h1>Welcome to MusPlay</h1>
      <p class="description">Your ultimate destination for music streaming</p>
      <router-link to="/api/login" class="btn btn-primary">Explore Now</router-link>
      <br>
      <router-link to="/about" class="btn btn-primary">About</router-link>
    </div>
    <div class="features">
      <div class="feature">
        <i class="fas fa-music"></i>
        <h2>Discover</h2>
        <p>Explore millions of songs across various genres and languages.</p>
      </div>
      <div class="feature">
        <i class="fas fa-headphones"></i>
        <h2>Listen</h2>
        <p>Stream music seamlessly on any device with high-quality audio.</p>
      </div>
      <div class="feature">
        <i class="fas fa-user-friends"></i>
        <h2>Connect</h2>
        <p>Connect with other music lovers, share playlists, and discover new favorites together.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  text-align: center;
}

.hero {
  background-image: url('../assets/home.jpg');
  background-size: cover;
  background-position: center;
  color: #fff;
  padding: 100px 20px;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.description {
  font-size: 24px;
  margin-bottom: 40px;
}

.btn {
  padding: 10px 20px;
  font-size: 18px;
  text-decoration: none;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}

.features {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 80px;
}

.feature {
  flex: 1;
  max-width: 300px;
}

.feature i {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.feature p {
  font-size: 18px;
}
</style>
