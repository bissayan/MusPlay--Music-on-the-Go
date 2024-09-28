<template>
    <div class="policy">
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
                  <router-link v-if="role !== 'admin' " to="/user_creator/1" class="nav-link">User</router-link>
                </li>  
                <li class="nav-item">
                  <router-link v-if="role === 'creator'" to="/creator" class="nav-link">Creator</router-link>
                </li>
                <li class="nav-item">
                  <router-link v-if="role === 'admin'" to="/api/admin" class="nav-link">Admin</router-link>
                </li>                              
              </ul>
              <button @click="logout()" class="btn btn-outline-primary" tabindex="-1" role="button">LogOut</button>              
            </div>
          </div>
        </nav>          
      </div>
      <br><br><br>
      <center>
          <div>
              <h4>If you are unable to access your Creator page and have been redirected here, you may have been blacklisted. Email the support team at musplay_support@gmail.com for further inquiry</h4>
              <h3>User Privacy and Data Security:</h3>
              <p>We prioritize the privacy and security of user data. All personal information collected, including listening habits and preferences, is treated with the utmost confidentiality. Users have control over their data and can manage privacy settings to tailor their experience. We commit to complying with applicable data protection laws and regularly updating our security measures.</p>

              <h3>Content Licensing and Copyright Compliance:</h3>
              <p>We respect the intellectual property rights of artists and content creators. Our app only streams music from authorized sources, ensuring that artists receive fair compensation for their work. Users are encouraged to report any potential copyright infringements, and we promptly address and rectify any such issues in compliance with copyright laws.</p>

              <h3>Inclusive and Responsible Content:</h3>
              <p>We strive to create an inclusive and respectful platform that celebrates diversity. Content that promotes hate speech, violence, or any form of discrimination is strictly prohibited. Users are encouraged to report any inappropriate content, and we reserve the right to take appropriate action, including content removal and account suspension, against violators of our community guidelines.</p>

              <h3>Device and Network Compatibility:</h3>
              <p>We are committed to providing a seamless and accessible music streaming experience across various devices and network conditions. Our app is optimized to work on a wide range of smartphones, tablets, and other compatible devices. We continuously improve app performance and responsiveness to ensure users can enjoy their favorite music without disruptions, even in varying network environments.</p>

              <h3>Community Engagement and Feedback:</h3>
              <p>We value user feedback and actively engage with our community to enhance the user experience. Users can provide feedback on the app's features, suggest improvements, and report issues through designated channels. Regular app updates are driven by user feedback, addressing reported issues and introducing new features that align with user preferences and industry trends. We are committed to transparent communication with our user community.</p>
          </div>
      </center>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
  data() {
    return {
      role: (JSON.parse(localStorage.getItem('user')).role)[0]
      
    };
  },
  methods: {
    fetchData() {
      const apiUrl = `http://localhost:5000/policy`;
      const accessToken = localStorage.getItem('access_token');      
      axios.get(apiUrl, {
      headers: {
          Authorization: `Bearer ${accessToken}`,
      },
      })
        .then(response => {          
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
  
  </style>
  