<template>
    <div class="login">
      <!--{% with messages = get_flashed_messages() %}  
        {% if messages %}  
          {% for message in messages %}  
            <p class="flash_message">{{ message }}</p>  
          {% endfor %}  
        {% endif %}  
      {% endwith %}-->
      
      <!--<button style="position:relative; overflow:hidden; float:right " type="submit" class="submit" name="/Go">Create Account</button>-->
  
      
        <div class="login-container">
          <h2>MusPlay</h2>          
            <form class="form" @submit.prevent="submitLogin" method="POST">
                  <div class="form-group">
                    <label for="username">User</label>
                    <input type="email" v-model="email_id" name="email_id" class="input" placeholder="Email" required>
                  </div>
                  <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" v-model="password" name="password" class="input" placeholder="Password" required>
                  </div>
                  
                    <button type="submit" @click="login" class="btn btn-primary">Login</button>
                  
              <div class="form-group">
                <router-link to="/forget_password" class="btn btn-link">Forgot Password?</router-link>
              </div>
              <div class="form-group">
                <router-link to="/admin_login" class="btn btn-success btn-lg active" role="button" aria-pressed="true">Admin</router-link>
              </div>
              <div class="form-group register-link">
                <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
              </div>
            </form>        
      </div>
    </div>  
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {        
        email_id: '',
        password: '',
        existing_emails:null,        
      };
    },
    created() {                
            this.DataChecker();                 
            },
    methods: {
      DataChecker() {      
      const apiUrl = 'http://localhost:5000/api/login';      
      axios.get(apiUrl)
        .then(response => {
          this.existing_emails = response.data[1]         
          console.log('Checking Data:', response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
      submitLogin() {
        const formData = {
          
          email_id: this.email_id,
          password: this.password,
          
        };
        
        if (this.existing_emails.includes(formData.email_id)){
        const apiUrl = 'http://localhost:5000/api/login';
        
        axios.post(apiUrl, formData)
          .then(response => {
            console.log(response.data);
                    const accessToken = response.data.access_token;
                    localStorage.setItem("access_token", accessToken);
                    const user = response.data.user; 
                    localStorage.setItem("user", JSON.stringify(user));
                    this.$store.commit('setAuthenticated', true);
                    this.$router.push("/user_creator/1");            
          })
          .catch(error => {
            console.error('Error logging in:', error);
            this.$router.push("/register");            
          });
        }
        else {
          console.log("You are not Registered");
          this.$router.push("/register");
        }
      },
    },
  
  };
  </script>
  
  <style scoped>
  body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }

        .login-container {
            max-width: 400px;
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

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .form-group button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .form-group button:hover {
            background-color: #0056b3;
        }

        .form-group .register-link {
            text-align: center;
            margin-top: 20px;
        }

        .form-group .register-link a {
            color: #007bff;
        }

        .form-group .register-link a:hover {
            text-decoration: underline;
        }

        .form-group .admin-btn {
            background-color: #28a745;
        }

        .form-group .admin-btn:hover {
            background-color: #218838;
        }
  </style>
  