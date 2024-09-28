<template>
  <div class="about-page">
    <div class="container">
      <h1>Welcome to Musplay</h1>
      <p class="mission">Your ultimate destination for music streaming!</p>
      
      <div class="section">
        <h2>Our Mission</h2>
        <p class="description">
          At Musplay, we are passionate about music and dedicated to providing users with the best streaming experience possible. Our mission is to connect people with their favorite songs, artists, and genres, while also introducing them to new music they'll love. Whether you're into chart-topping hits or hidden gems, Musplay has something for everyone.
        </p>
      </div>

      <div class="section">
        <h2>What Sets Us Apart</h2>
        <ul class="features">
          <li><strong>Personalized Recommendations:</strong> Our advanced recommendation algorithms analyze your listening habits to suggest music tailored to your tastes.</li>
          <li><strong>Extensive Music Library:</strong> With millions of songs spanning various genres and languages, Musplay offers one of the most comprehensive music libraries available.</li>
          <li><strong>High-Quality Audio:</strong> Experience music like never before with crystal-clear, high-fidelity audio streaming.</li>
          <li><strong>Cross-Platform Compatibility:</strong> Musplay is available on all major platforms, ensuring seamless listening across devices.</li>
        </ul>
      </div>

      <div class="section">
        <h2>Our Team</h2>
        <p class="description">
          Behind Musplay is a team of dedicated music enthusiasts, developers, and creatives who share a common goal: to revolutionize the way people discover and enjoy music. We're constantly innovating and striving to enhance the Musplay experience for our users.
        </p>
      </div>

      <div class="section">
        <h2>Get Started Today!</h2>
        <p class="description">
          Join the Musplay community today and embark on a musical journey like no other. Sign up for a free account to unlock unlimited access to our vast music library, curated playlists, exclusive content, and much more. Whether you're a casual listener or a die-hard music fan, Musplay has everything you need to soundtrack your life. Reach out to us at musplay_support@gmail.com .
        </p>
      </div>

      <p class="thank-you">Thank you for choosing Musplay. Let the music play! 🎶</p>
      <router-link to="/api/login" class="btn btn-primary">Explore Now</router-link>&nbsp;
      <router-link to="/" class="btn btn-primary">Home</router-link>  
    </div>    
  </div>  
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  font-size: 36px;
  margin-bottom: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.mission {
  font-size: 20px;
  margin-bottom: 40px;
}

.section {
  margin-bottom: 40px;
}

.features {
  list-style-type: none;
  padding-left: 0;
}

.features li {
  margin-bottom: 10px;
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


.thank-you {
  font-style: italic;
  text-align: center;
  margin-top: 40px;
}
</style>
