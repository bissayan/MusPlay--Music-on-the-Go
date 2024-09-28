<template>
    <div class="admin_login">
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
            <form class="form">
                  <div class="form-group">
                    <label for="username">User</label>
                    <input type="email" v-model="email_id" name="email_id" class="input" placeholder="Email" required>
                  </div>
                  <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" v-model="password" name="password" class="input" placeholder="Password" required>
                  </div>
                  
                    <button @click.prevent="submitLogin" class="btn btn-primary">Login</button>                  
              
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
      };
    },    
    methods: {      
      submitLogin() {
        const formData = {
          
          email_id: this.email_id,
          password: this.password,
          
        };
        
        if (formData.email_id=='musplayadmin@gmail.com'){
            if(formData.password==6789){
        const apiUrl = 'http://localhost:5000/api/login';
        
        axios.post(apiUrl,{"email_id": this.email_id, "password": this.password})
          .then(response => {
                    console.log(response.data.roles);
                    const accessToken = response.data.access_token;
                    localStorage.setItem("access_token", accessToken);
                    const user = response.data.user; 
                    localStorage.setItem("user", JSON.stringify(user));                    
            this.$router.push("/admin_support");
            
          })
          .catch(error => {
            console.error('Error logging in:', error);
          });          
        }
        else {
          console.log("Incorrect Password");
          this.$router.push("/admin_login");
        }
    }
        else {
          console.log("You do not have Admin Accesss");
          this.$router.push("/api/login");
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
  