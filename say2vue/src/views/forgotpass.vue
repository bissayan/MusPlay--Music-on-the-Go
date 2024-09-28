<template>
    <div class="forgotpass">     
        <div class="register-container">
          <h2>MusPlay</h2> 
          <form class="form" @submit.prevent="submitForm" method="POST">
             
            <div class="form-group">
              <label for="email_id">Email</label>
              <input v-model="email_id" type="email" name="email_id" class="input" placeholder="Email" required>
            </div>  
            <div class="form-group">
              <label for="password">Password</label>
              <input v-model="password" type="password" name="password" class="input" placeholder="Password" required>
            </div>  
            <div class="form-group">
              <label for="confirm_password">Confirm Password</label>
              <input v-model="confirm_password" type="password" name="confirm_password" class="input" placeholder="Confirm Password" required>
            </div>            
            <button type="submit" @click="register" class="btn btn-primary">Chnage Password</button>            
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
        confirm_password: '',
        existing_emails:null,        
      };
    },
    created() {                
            this.DataChecker();                 
            },
    methods: {
      DataChecker() {      
      const apiUrl = 'http://localhost:5000/forget_password';      
      axios.get(apiUrl)
        .then(response => {
          this.existing_emails = response.data         
          console.log('Checking Data:', response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
      submitForm() {
        const formData = {
          
          email_id: this.email_id,
          password: this.password,
          confirm_password: this.confirm_password,          
        };
  
        const apiUrl = 'http://localhost:5000/forget_password';
        if (this.existing_emails.includes(formData.email_id)){
          if(formData.password==formData.confirm_password){
            axios.post(apiUrl, formData)
              .then(response => {
                console.log(response.data);

                this.$router.push("/api/login");                
              })
              .catch(error => {
                console.error('Error registering:', error);                
              });
            }
          else {
            console.log("Passwords Don't Match");
          }       
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

        .register-container {
            max-width: 400px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.3s;
        }

        .regsiter-container:hover {
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
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
        
  </style>
  